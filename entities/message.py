from enum import Enum
from tortoise.models import Model
from tortoise import fields

from entities.mixins import IdMixin, DatetimeMixin

class MessageEnumType(Enum):
    TEXT: str = "TEXT"
    IMAGE: str = "IMAGE"

class MessageEntity(Model, IdMixin, DatetimeMixin):
    chat = fields.ForeignKeyField("models.ChatEntity", related_name="messages")
    content = fields.TextField()
    content_type = fields.CharEnumField(MessageEnumType)
    user_author = fields.ForeignKeyField("models.UserEntity", related_name=None)

