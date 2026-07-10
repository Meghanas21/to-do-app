from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.exceptions.custom_exceptions import PermissionDeniedError, TaskNotFoundError


class TaskService:
    def list_tasks(self, db: Session, current_user: User, status: Optional[str] = None, assigned_to: Optional[int] = None) -> List[Task]:
        query = db.query(Task)
        if current_user.role and current_user.role.name != "admin":
            query = query.filter(Task.assigned_to_id == current_user.id)
        if status:
            query = query.filter(Task.status == status.lower())
        if assigned_to is not None:
            query = query.filter(Task.assigned_to_id == assigned_to)
        return query.order_by(Task.created_at.desc()).all()

    def create_task(self, db: Session, current_user: User, task_in: TaskCreate) -> Task:
        if not current_user.role or current_user.role.name != "admin":
            raise PermissionDeniedError("Only admins can create tasks.")
        task = Task(
            title=task_in.title,
            description=task_in.description,
            created_by_id=current_user.id,
            assigned_to_id=task_in.assigned_to_id,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def update_task_status(self, db: Session, current_user: User, task_id: int, task_in: TaskUpdate) -> Task:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskNotFoundError(task_id)
        if current_user.role and current_user.role.name != "admin" and task.assigned_to_id != current_user.id:
            raise PermissionDeniedError("You can only update tasks assigned to you.")
        if task_in.status:
            task.status = task_in.status.lower()
        db.commit()
        db.refresh(task)
        return task


task_service = TaskService()
