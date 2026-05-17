from typing import Any, Optional


def success_response(data: Any, message: Optional[str] = None) -> dict:
    return {"data": data, "message": message, "error": None}


def error_response(message: str) -> dict:
    return {"data": None, "message": message, "error": message}
