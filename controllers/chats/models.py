# controllers/chat/models.py
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

from controllers.auth.models import UserResponse
from controllers.conversations.models import PersonalityResponse

class ChatCreateDTO(BaseModel):
    name: str
    vectorstore_path: str
    config: dict
    personality_id: Optional[int] = None


class ChatUpdateDTO(BaseModel):
    name: str
    vectorstore_path: Optional[str] = None
    config: Optional[dict] = None


class ChatResponse(BaseModel):
    id: int
    name: str
    vectorstore_path: str
    config: dict
    created_by: UserResponse
    invited_users: list[UserResponse]
    personality_id: Optional[int] = None
    personality: Optional[PersonalityResponse] = None
    created_at: datetime
    updated_at: datetime