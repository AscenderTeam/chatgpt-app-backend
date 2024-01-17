from datetime import datetime
from typing import Literal
from pydantic import BaseModel

from entities.message import AuthorTypeEnum, MessageEnumType


class MessageDTO(BaseModel):
    content: str
    image_url: str | None = None
    content_type: MessageEnumType = MessageEnumType.TEXT
    author_type: AuthorTypeEnum = AuthorTypeEnum.USER
    chat_id: int


class MessageResponse(MessageDTO):
    id: int
    created_at: datetime
    updated_at: datetime