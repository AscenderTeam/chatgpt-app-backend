from __future__ import annotations
from typing import TYPE_CHECKING
from tortoise.models import Model
from tortoise import fields
from entities.mixins import IdMixin, DatetimeMixin

from entities.message import MessageEntity



class ChatEntity(Model, IdMixin, DatetimeMixin):
    name = fields.CharField(max_length=100)
    vectorstore_path = fields.TextField()
    config = fields.JSONField()
    created_by = fields.ForeignKeyField("models.UserEntity", related_name="chats")
    messages = fields.ReverseRelation("models.MessageEntity", relation_field="messages", instance=MessageEntity, from_field="chat")
    # Many-to-many relation for invited users
    invited_users = fields.ManyToManyField(
        'models.UserEntity',
        related_name='invited_to_chats',
    )