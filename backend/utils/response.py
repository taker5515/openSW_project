from typing import Any, Optional


def success_response(data: Any, message: Optional[str] = None) -> dict:
    return {"success": True, "data": data, "message": message}


def error_response(message: str) -> dict:
    return {"success": False, "data": None, "message": message}
