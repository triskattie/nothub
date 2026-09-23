from typing import Any

class AppError(Exception):
    status_code = 500
    code = "internal_error"
    title = "Internal Server Error"

    def __init__(self, detail: str, *, context: dict[str, Any] | None = None) -> None:
        super().__init__(detail)
        self.detail = detail
        self.context = context or {}


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"
    title = "Resource Not Found"