from pydantic import BaseModel

from entities.message import MessageEnumType


class MessageDTO(BaseModel):
    content: str
    content_type: MessageEnumType = MessageEnumType.TEXT
    chat_id: int