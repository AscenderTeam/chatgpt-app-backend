from tortoise.models import Model
from tortoise import fields

from entities.mixins import IdMixin, DatetimeMixin


class ChatEntity(Model, IdMixin, DatetimeMixin):
    vectorstore_path = fields.CharField(max_length=1000, unique=True)
    config = fields.JSONField()
    created_by = fields.ForeignKeyField("models.UserEntity", related_name="chats")
    messages = fields.ReverseRelation["Message"]
    # Many-to-many relation for invited users
    invited_users = fields.ManyToManyField(
        'models.UserEntity',
        related_name='invited_to_chats',
    )