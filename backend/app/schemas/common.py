from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Consistent error shape returned by every exception handler."""
    detail: str
