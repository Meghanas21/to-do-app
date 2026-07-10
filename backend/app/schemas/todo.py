from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = ""

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoOut(TodoBase):
    id: int
    completed: bool
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
