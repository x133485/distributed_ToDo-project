from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware


# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Test Page"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有头部
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user.username, user.password)


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # 返回一个假token
    return {"token": f"token_for_{user.username}"}


@app.post("/validate_user")
def validate_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user and db_user.password == user.password:
        return {"status": "valid"}
    else:
        raise HTTPException(status_code=401, detail="Invalid user")
