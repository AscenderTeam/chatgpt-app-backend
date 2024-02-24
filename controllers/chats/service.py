from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import HTTPException
from controllers.auth.models import UserResponse
from controllers.chats.serializer import ChatSerializer
from controllers.conversations.models import MessageDTO
from controllers.сommon.models.pagination import PaginatedResponse, PaginationMeta
from core.extensions.serializer import QuerySetSerializer
from core.extensions.services import Service
from controllers.chats.repository import ChatRepo
from controllers.chats.models import ChatCreateDTO, ChatResponse, ChatUpdateDTO
from entities.chat import ChatEntity
from entities.message import AuthorTypeEnum

if TYPE_CHECKING:
    from controllers.conversations.endpoints import Conversations

class ChatService(Service):
    conversations: Conversations

    def __init__(self, repository: ChatRepo):
        self.repository = repository

    async def create_chat(self, chat: ChatCreateDTO, user: UserResponse):
        chat: ChatEntity = await self.repository.create_chat(chat, user.id)
        if chat.personality:
            self.inject_controller("Conversations", "conversations")
            await self.conversations.conversations_service._repository.create_message(user.id, **MessageDTO(
            content=chat.personality.first_message,
            chat_id=chat.id,
            author_type=AuthorTypeEnum.AI,
        ).model_dump())
        return ChatSerializer(None, chat)()

    async def invite_to_chat(self, chat_id: int, member_ids: list[int], user: UserResponse):
        try:
            invited_users = await self.repository.add_users_to_chat(chat_id, user.id, *member_ids)
        except:
            raise HTTPException(404, "User invited to chat not found")
        
        if not invited_users:
            raise HTTPException(404, "Chat not found")

        return ChatSerializer(None, invited_users)()

    async def get_invited_chat(self, chat_id: int, user: UserResponse):
        return await self.repository.get_invited_chat(chat_id, user.id)
    
    async def get_invited_chats(self, user: UserResponse):
        return await self.repository.get_invited_chats(user.id)

    async def get_chat(self, chat_id: int, user: UserResponse) -> ChatResponse:
        chat = await self.repository.get_chat(chat_id, user.id)
        if not chat:
            raise HTTPException(404, "Chat not found")

        return ChatSerializer(ChatResponse, chat)()

    async def get_chats(self, user: UserResponse):
        chats = await self.repository.get_chats(user.id)
        return list(QuerySetSerializer.serialize_queryset(ChatSerializer, ChatResponse, chats))

    async def get_chats_paginated(self, user: UserResponse, page: int = 1, page_size: int = 10):
        # Implementing pagiantion, converting into offset and getting count of the chats
        offset = (page - 1) * page_size
        chats = await self.repository.get_chats_offsetted(user.id, offset, page_size)

        # Getting count of the chats
        count = await self.repository.get_chats_count(user.id)

        # Paginated response
        return PaginatedResponse(
            data=list(QuerySetSerializer.serialize_queryset(ChatSerializer, ChatResponse, chats)),
            meta=PaginationMeta(
                items_count=count,
                page=page,
                page_size=page_size,
                total_pages=count // page_size
            )
        )

    async def update_chat(self, chat_id: int, chat: ChatUpdateDTO):
        updated_chat = await self.repository.update_chat(chat_id, chat)
        return ChatSerializer(None, updated_chat)()

    async def delete_chat(self, chat_id: int, user: UserResponse):
        _deleted_chat = await self.repository.delete_chat(chat_id, user.id)
        if not _deleted_chat:
            raise HTTPException(404, "Chat not found")
        return _deleted_chat