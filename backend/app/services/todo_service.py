"""
Business logic for todo CRUD, always scoped to the requesting user so one
user can never read/edit/delete another user's todos.
"""
from typing import List
from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate
from app.exceptions.custom_exceptions import TodoNotFoundError


def list_todos(db: Session, owner: User) -> List[Todo]:
    return db.query(Todo).filter(Todo.owner_id == owner.id).all()


def get_todo(db: Session, owner: User, todo_id: int) -> Todo:
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == owner.id).first()
    if not todo:
        raise TodoNotFoundError(todo_id)
    return todo


def create_todo(db: Session, owner: User, todo_in: TodoCreate) -> Todo:
    todo = Todo(**todo_in.model_dump(), owner_id=owner.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update_todo(db: Session, owner: User, todo_id: int, todo_in: TodoUpdate) -> Todo:
    todo = get_todo(db, owner, todo_id)
    update_data = todo_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, owner: User, todo_id: int) -> None:
    todo = get_todo(db, owner, todo_id)
    db.delete(todo)
    db.commit()
