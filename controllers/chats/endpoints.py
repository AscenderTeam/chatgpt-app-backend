# controllers/chat/endpoints.py
from fastapi import Body, Depends

from controllers.auth.models import UserResponse
from controllers.chats.repository import ChatRepo
from core.guards.authenticator import GetAuthenticatedUser
from core.types import ControllerModule
from core.utils.controller import Controller, Get, Post, Put, Delete
from controllers.chats.service import ChatService
from controllers.chats.models import ChatCreateDTO, ChatUpdateDTO, ChatResponse

@Controller()
class ChatController:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    @Post(response_model=ChatResponse)
    async def create_chat(self, chat: ChatCreateDTO, user: UserResponse = Depends(GetAuthenticatedUser(True))):
        return await self.chat_service.create_chat(chat, user)

    @Get("/{chat_id}")
    async def get_chat(self, chat_id: int, user: UserResponse = Depends(GetAuthenticatedUser(True))):
        return await self.chat_service.get_chat(chat_id, user)

    @Put("/{chat_id}")
    async def update_chat(self, chat_id: int, chat: ChatUpdateDTO, user: UserResponse = Depends(GetAuthenticatedUser(True))):
        return await self.chat_service.update_chat(chat_id, chat)

    @Delete("/{chat_id}")
    async def delete_chat(self, chat_id: int, user: UserResponse = Depends(GetAuthenticatedUser(True))):
        return await self.chat_service.delete_chat(chat_id, user)
    
    @Post("/{chat_id}/invite/")
    async def invite_user_to_chat(self, chat_id: int, member_ids: list[int] = Body(), user: UserResponse = Depends(GetAuthenticatedUser(True))):
        return await self.chat_service.invite_to_chat(chat_id=chat_id, member_ids=member_ids, user=user)
    
    @Get()
    async def get_chats(self, page: int = 1, page_size: int = 10, user: UserResponse = Depends(GetAuthenticatedUser(True))):
        return await self.chat_service.get_chats_paginated(user=user, page=page, page_size=page_size)


def setup() -> ControllerModule:
    return {
        "controller": ChatController,
        "services": {
            "chat": ChatService,
        },
        "repository": ChatRepo,
        "repository_entities": {
        }
    }
