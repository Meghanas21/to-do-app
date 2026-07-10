import json
from io import BytesIO
from typing import List
from sqlalchemy.orm import Session
from pypdf import PdfReader

from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentOut
from app.exceptions.custom_exceptions import PermissionDeniedError
from app.services.vector_service import vector_store


class DocumentService:
    def list_documents(self, db: Session) -> List[Document]:
        return db.query(Document).order_by(Document.created_at.desc()).all()

    def upload_document(self, db: Session, current_user: User, title: str, filename: str, content_type: str, content_text: str, metadata: dict | None = None) -> Document:
        if not current_user.role or current_user.role.name != "admin":
            raise PermissionDeniedError("Only admins can upload documents.")
        document = Document(
            title=title,
            filename=filename,
            content_type=content_type,
            content_text=content_text,
            metadata_json=json.dumps(metadata or {}),
            uploaded_by_id=current_user.id,
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        vector_store.add_document(document.id, document.title, document.content_text)
        return document

    def parse_upload(self, filename: str, content_type: str, file_bytes: bytes) -> str:
        if filename.lower().endswith(".pdf"):
            reader = PdfReader(BytesIO(file_bytes))
            return "\n\n".join(page.extract_text() or "" for page in reader.pages)
        return file_bytes.decode("utf-8", errors="ignore")

    def search_documents(self, db: Session, query: str, limit: int = 5) -> List[DocumentOut]:
        documents = db.query(Document).all()
        if documents and not vector_store.documents:
            vector_store.rebuild([{"id": doc.id, "title": doc.title, "content_text": doc.content_text} for doc in documents])

        matches = vector_store.search(query, limit=limit)
        if not matches:
            return []
        document_ids = [doc_id for doc_id, _score in matches]
        documents = db.query(Document).filter(Document.id.in_(document_ids)).all()
        doc_map = {document.id: document for document in documents}
        ordered = [doc_map[doc_id] for doc_id in document_ids if doc_id in doc_map]
        return [DocumentOut.model_validate(document) for document in ordered]


document_service = DocumentService()
