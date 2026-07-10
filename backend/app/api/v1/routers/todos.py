import logging
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.todo import TodoCreate, TodoUpdate, TodoOut
from app.services import todo_service
from app.api.deps import get_current_user
from app.models.user import User

logger = logging.getLogger("todo_api")

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])


@router.get("", response_model=List[TodoOut])
def list_todos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return todo_service.list_todos(db, current_user)


@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_in: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = todo_service.create_todo(db, current_user, todo_in)
    logger.info("Todo %s created by %s", todo.id, current_user.email)
    return todo


@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return todo_service.get_todo(db, current_user, todo_id)


@router.put("/{todo_id}", response_model=TodoOut)
def update_todo(
    todo_id: int,
    todo_in: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = todo_service.update_todo(db, current_user, todo_id, todo_in)
    logger.info("Todo %s updated by %s", todo.id, current_user.email)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo_service.delete_todo(db, current_user, todo_id)
    logger.info("Todo %s deleted by %s", todo_id, current_user.email)
    return None
