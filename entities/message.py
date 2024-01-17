from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum
from tortoise.models import Model
from tortoise import fields
from core.extensions.authentication.entity import UserEntity

from entities.mixins import IdMixin, DatetimeMixin

if TYPE_CHECKING:
    from entities.chat import ChatEntity

class MessageEnumType(Enum):
    TEXT: str = "TEXT"
    IMAGE: str = "IMAGE"


class AuthorTypeEnum(Enum):
    AI: str = "AI"
    USER: str = "User"


class MessageEntity(Model, IdMixin, DatetimeMixin):
    chat: ChatEntity = fields.ForeignKeyField("models.ChatEntity", related_name="messages")
    content: str = fields.TextField()
    content_type: MessageEnumType = fields.CharEnumField(MessageEnumType)
    author_type: AuthorTypeEnum = fields.CharEnumField(AuthorTypeEnum)
    user_author: UserEntity = fields.ForeignKeyField("models.UserEntity", null=True)

