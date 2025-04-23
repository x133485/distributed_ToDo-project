from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from task_service.database import SessionLocal, engine, Base
from task_service import crud, models
import httpx
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_token(token: str = Header(...)):
    try:
        res = requests.post("http://localhost:8000/validate_user", json={"token": token})
        data = res.json()
        if res.status_code == 200 and data.get("valid"):
            return data["user_id"]
    except Exception as e:
        print(f"Token 验证失败：{e}")
    raise HTTPException(status_code=401, detail="Invalid token")

class TaskCreate(BaseModel):
    title: str
    content: str

class TaskUpdate(BaseModel):
    title: str
    content: str

class PublicTaskCreate(BaseModel):
    title: str
    content: str
    channel_code: str

async def validate_user(token: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/validate_user",
                json={"token": token},
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="User Service unavailable")

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    token = authorization.split("Bearer ")[-1]
    user_info = await validate_user(token)
    if not user_info.get("valid"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_info["user_id"]

@app.post("/tasks")
async def create_task(task: TaskCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = crud.create_task(db, user_id=user_id, title=task.title, content=task.content)
    return {"id": db_task.id, "title": db_task.title, "content": db_task.content, "user_id": db_task.user_id}

@app.get("/tasks")
async def read_tasks(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = crud.get_user_tasks(db, user_id=user_id)
    task_list = []
    for t in tasks:
        task_list.append({
            "id": t.id,
            "title": t.title,
            "content": t.content,
            "user_id": t.user_id,
            "is_public": t.is_public,
            "channel_code": t.channel_code,
            "editable": True if t.is_public else False
        })
    return task_list

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskUpdate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    updated_task = crud.update_task(db, task_id=task_id, title=task.title, content=task.content)
    return {"id": updated_task.id, "title": updated_task.title, "content": updated_task.content}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    crud.delete_task(db, task_id=task_id)
    return {"message": "Task deleted successfully"}

@app.post("/public_tasks/create")
async def create_public_task(task: PublicTaskCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_public_task(
        db, user_id=user_id,
        title=task.title, content=task.content, channel_code=task.channel_code
    )

@app.get("/public_tasks/{code}")
async def get_public_task(code: str, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task = crud.get_task_by_channel_code(db, code)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": task.id,
        "title": task.title,
        "content": task.content,
        "channel_code": task.channel_code,
        "user_id": task.user_id,
        "editable": task.user_id == user_id
    }

@app.put("/public_tasks/{task_id}")
async def update_public(task_id: int, task: TaskUpdate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_public_task(db, task_id=task_id, user_id=user_id, title=task.title, content=task.content)

@app.delete("/public_tasks/{task_id}")
async def delete_public(task_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.delete_public_task(db, task_id=task_id, user_id=user_id)
