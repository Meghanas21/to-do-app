from typing import List, Optional
from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.document import DocumentOut
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.schemas.analytics import AnalyticsOut
from app.schemas.user import UserOut
from app.services.analytics_service import analytics_service
from app.services.document_service import document_service
from app.services.task_service import task_service
from app.services.activity_service import activity_service

router = APIRouter(prefix="/api/v1", tags=["knowledge"])


@router.get("/tasks", response_model=List[TaskOut])
def list_tasks(
    status: Optional[str] = Query(None),
    assigned_to: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = task_service.list_tasks(db, current_user, status=status, assigned_to=assigned_to)
    return tasks


@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = task_service.create_task(db, current_user, task_in)
    activity_service.log_action(db, current_user.id, "task_create", f"Created task {task.title}")
    return task


@router.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = task_service.update_task_status(db, current_user, task_id, task_in)
    activity_service.log_action(db, current_user.id, "task_update", f"Updated task {task.id} to {task.status}")
    return task


@router.get("/documents", response_model=List[DocumentOut])
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return document_service.list_documents(db)


@router.post("/documents", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def upload_document(
    title: str = "",
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content_text = document_service.parse_upload(file.filename or "upload.txt", file.content_type or "text/plain", file.file.read())
    safe_title = title or (file.filename or "Uploaded document")
    document = document_service.upload_document(
        db,
        current_user,
        safe_title,
        file.filename or "upload.txt",
        file.content_type or "text/plain",
        content_text,
        metadata={"source": "upload"},
    )
    activity_service.log_action(db, current_user.id, "document_upload", f"Uploaded document {document.title}")
    return document


@router.post("/search", response_model=List[DocumentOut])
def search_documents(query: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    activity_service.log_action(db, current_user.id, "search", query)
    return document_service.search_documents(db, query)


@router.get("/analytics", response_model=AnalyticsOut)
def get_analytics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.get_analytics(db)


@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    return [UserOut(id=user.id, email=user.email, role_name=user.role.name if user.role else None) for user in users]
