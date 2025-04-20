from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from task_service.database import SessionLocal, engine, Base
from task_service import crud, models
import httpx

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖注入数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 数据模型
class TaskCreate(BaseModel):
    title: str
    content: str

class TaskUpdate(BaseModel):
    title: str
    content: str

# User Service 验证接口地址
USER_SERVICE_URL = "http://localhost:8000/validate_user"

# task_service/app.py
async def validate_user(token: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/validate_user",
                json={"token": token},  # 确保字段名正确
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="User Service unavailable")

# 用户验证中间件
async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    token = authorization.split("Bearer ")[-1]
    user_info = await validate_user(token)
    if not user_info.get("valid"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_info["user_id"]

# 接口实现
@app.post("/tasks")
async def create_task(
    task: TaskCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = crud.create_task(db, user_id=user_id, title=task.title, content=task.content)
    return {"id": db_task.id, "title": db_task.title, "content": db_task.content}

@app.get("/tasks")
async def read_tasks(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = crud.get_user_tasks(db, user_id=user_id)
    return [{"id": t.id, "title": t.title, "content": t.content} for t in tasks]

@app.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task: TaskUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = crud.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    updated_task = crud.update_task(db, task_id=task_id, title=task.title, content=task.content)
    return {"id": updated_task.id, "title": updated_task.title, "content": updated_task.content}

@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = crud.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    crud.delete_task(db, task_id=task_id)
    return {"message": "Task deleted successfully"}