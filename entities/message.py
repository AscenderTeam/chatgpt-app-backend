from tortoise.models import Model
from tortoise import fields

from entities.mixins import IdMixin, DatetimeMixin


class Message(Model, IdMixin, DatetimeMixin):
    chat = fields.ForeignKeyField("models.ChatEntity", related_name="messages")
    content = fields.TextField()
    type = fields.CharField(max_length=100)
    user_author = fields.ForeignKeyField("models.UserEntity", related_name=None)

