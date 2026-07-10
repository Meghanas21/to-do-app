from typing import Optional
from pydantic import BaseModel, ConfigDict


class DocumentCreate(BaseModel):
    title: str
    filename: str
    content_type: str
    content_text: str
    metadata: Optional[dict] = None


class DocumentOut(BaseModel):
    id: int
    title: str
    filename: str
    content_type: str
    content_text: str
    metadata_json: Optional[str] = None
    uploaded_by_id: int

    model_config = ConfigDict(from_attributes=True)
