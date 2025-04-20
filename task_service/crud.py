from sqlalchemy.orm import Session
from task_service.models import Task  # 绝对路径

def create_task(db: Session, user_id: int, title: str, content: str):
    db_task = Task(user_id=user_id, title=title, content=content)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_user_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()

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