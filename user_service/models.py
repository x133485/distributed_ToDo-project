from sqlalchemy import Column, Integer, String
from user_service.database import Base  # 必须使用完整路径

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    token = Column(String, unique=True, index=True)  # 新增 token 字段
