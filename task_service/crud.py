from sqlalchemy.orm import Session
from task_service.models import Task  # 绝对路径
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy import or_, and_
from task_service.database import Base
from fastapi import HTTPException
import uuid

def create_task(db: Session, user_id: int, title: str, content: str):
    db_task = Task(user_id=user_id, title=title, content=content)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_user_tasks(db: Session, user_id: int):
    return db.query(Task).filter(
        or_(
            Task.user_id == user_id,
            and_(Task.user_id == user_id, Task.is_public == True)
        )
    ).all()


def update_task(db: Session, task_id: int, title: str, content: str):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.title = title
        db_task.content = content
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def create_public_task(db: Session, user_id: int, title: str, content: str, channel_code: str):
    # print(f"创建公共任务: 用户 {user_id}, 标题 {title}, 频道码 {channel_code}")  # 用于调试

    task = Task(
        user_id=user_id,
        title=title,
        content=content,
        is_public=True,
        channel_code=channel_code  # ✅ 使用前端传入的频道码
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_by_channel_code(db: Session, code: str):
    return db.query(Task).filter(Task.channel_code == code, Task.is_public == True).first()

def update_public_task(db: Session, task_id: int, user_id: int, title: str, content: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the creator")
    task.title = title
    task.content = content
    db.commit()
    return task

def get_task_by_channel_code(db: Session, channel_code: str):
    return db.query(Task).filter(Task.channel_code == channel_code).first()

def delete_public_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the creator")
    db.delete(task)
    db.commit()
    return {"message": "Deleted"}
