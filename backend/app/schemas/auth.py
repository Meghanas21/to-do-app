from pydantic import BaseModel, ConfigDict


class UserSummary(BaseModel):
    id: int
    email: str
    role_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
