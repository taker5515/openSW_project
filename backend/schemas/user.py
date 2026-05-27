from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# TODO: Expand when user profile features are implemented


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: Optional[datetime] = None
