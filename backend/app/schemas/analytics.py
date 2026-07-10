from pydantic import BaseModel


class AnalyticsOut(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    most_searched_query: str | None = None
    most_searched_count: int = 0
