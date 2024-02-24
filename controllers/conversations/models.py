from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel
from controllers.auth.models import UserResponse

from entities.message import AuthorTypeEnum, MessageEnumType


class MessageDTO(BaseModel):
    content: str
    image_url: str | None = None
    content_type: MessageEnumType = MessageEnumType.TEXT
    author_type: AuthorTypeEnum = AuthorTypeEnum.USER
    chat_id: int


class MessageResponse(MessageDTO):
    id: int
    author: Optional[UserResponse] = None
    created_at: datetime
    updated_at: datetime


class PersonalityResponse(BaseModel):
    id: int
    name: str
    appearance: str
    description: str
    first_message: str