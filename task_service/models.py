from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from task_service.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String)
    content = Column(Text)
    created_at = Column(String)
    updated_at = Column(String)
    is_public = Column(Boolean, default=False)
    channel_code = Column(String, unique=True, default=None)
