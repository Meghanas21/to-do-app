"""
Domain-specific exceptions. Services raise these; a global handler in
main.py converts them into consistent JSON error responses. This keeps
services free of HTTP-specific concerns (status codes belong to the web
layer, not the business logic layer).
"""


class AppError(Exception):
    """Base class for all domain errors."""
    status_code: int = 400

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class DuplicateEmailError(AppError):
    status_code = 409

    def __init__(self, email: str):
        super().__init__(f"An account with email '{email}' already exists.")


class InvalidCredentialsError(AppError):
    status_code = 401

    def __init__(self):
        super().__init__("Incorrect email or password.")


class TodoNotFoundError(AppError):
    status_code = 404

    def __init__(self, todo_id: int):
        super().__init__(f"Todo with id {todo_id} was not found.")


class TaskNotFoundError(AppError):
    status_code = 404

    def __init__(self, task_id: int):
        super().__init__(f"Task with id {task_id} was not found.")


class PermissionDeniedError(AppError):
    status_code = 403

    def __init__(self, detail: str):
        super().__init__(detail)


class NotAuthenticatedError(AppError):
    status_code = 401

    def __init__(self):
        super().__init__("Could not validate credentials.")
