# controllers/chat/endpoints.py
from fastapi import Depends

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

    @Post("/chats", response_model=ChatCreateDTO)
    async def create_chat(self, chat: ChatCreateDTO, user: UserResponse = Depends(GetAuthenticatedUser(True))):
        return await self.chat_service.create_chat(chat, user)

    @Get("/chats/{chat_id}")
    async def get_chat(self, chat_id: int, user: UserResponse = Depends(GetAuthenticatedUser(True))):
        return await self.chat_service.get_chat(chat_id, user)

    @Put("/chats/{chat_id}")
    async def update_chat(self, chat_id: int, chat: ChatUpdateDTO, user: UserResponse = Depends(GetAuthenticatedUser(True))):
        return await self.chat_service.update_chat(chat_id, chat)

    @Delete("/chats/{chat_id}")
    async def delete_chat(self, chat_id: int, user: UserResponse = Depends(GetAuthenticatedUser(True))):
        return await self.chat_service.delete_chat(chat_id)

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
