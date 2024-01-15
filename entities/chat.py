from tortoise.models import Model
from tortoise import fields

from entities.mixins import IdMixin, DatetimeMixin


class ChatEntity(Model, IdMixin, DatetimeMixin):
    name = fields.CharField(max_length=100)
    vectorstore_path = fields.TextField(unique=True)
    config = fields.JSONField()
    created_by = fields.ForeignKeyField("models.UserEntity", related_name="chats")
    messages = fields.ReverseRelation("Message")
    # Many-to-many relation for invited users
    invited_users = fields.ManyToManyField(
        'models.UserEntity',
        related_name='invited_to_chats',
    )  # if more than 0, that's a group chat!
