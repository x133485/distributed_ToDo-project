from sqlalchemy.orm import Session
from user_service.models import User  # 绝对路径
import uuid

def create_user(db: Session, username: str, password: str):
    # 生成唯一 Token
    token = str(uuid.uuid4())
    # 创建用户时保存 Token
    db_user = User(username=username, password=password, token=token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
def get_user_by_token(db: Session, token: str):
    return db.query(User).filter(User.token == token).first()