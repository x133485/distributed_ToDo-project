from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import uuid4
# 关键修改点 ↓↓↓
from user_service.database import SessionLocal, engine, Base
from user_service import crud, models
 # 相对导入

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 数据模型
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenValidationRequest(BaseModel):
    token: str  # 仅接收 token 字段

# 接口实现
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password too short")
    
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return crud.create_user(db, user.username, user.password)

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 生成唯一 Token 并保存到数据库
    token = str(uuid4())
    db_user.token = token
    db.commit()
    db.refresh(db_user)
    
    return {"token": token}

@app.post("/validate_user")
def validate_user(request: TokenValidationRequest, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_token(db, request.token)  # 根据 token 查询用户
    if db_user:
        return {"valid": True, "user_id": db_user.id}
    return {"valid": False}