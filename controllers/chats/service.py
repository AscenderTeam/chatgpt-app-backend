from fastapi import HTTPException
from controllers.auth.models import UserResponse
from core.extensions.services import Service
from controllers.chats.repository import ChatRepo
from controllers.chats.models import ChatCreateDTO, ChatUpdateDTO

class ChatService(Service):
    def __init__(self, repository: ChatRepo):
        self.repository = repository

    async def create_chat(self, chat: ChatCreateDTO):
        return await self.repository.create_chat(chat)

    async def invite_to_chat(self, chat_id: int, member_ids: list[int], user: UserResponse):
        try:
            invited_users = await self.repository.add_users_to_chat(chat_id, user.id, *member_ids)
        except:
            raise HTTPException(404, "User invited to chat not found")
        
        if not invited_users:
            raise HTTPException(404, "Chat not found")

        return invited_users

    async def get_invited_chats(self, chat_id: int, user: UserResponse):
        return await self.repository.get_invited_chats(chat_id, user.id)

    async def get_chat(self, chat_id: int, user: UserResponse):
        chat = await self.repository.get_chat(chat_id, user)
        if not chat:
            raise HTTPException(404, "Chat not found")

        return chat

    async def get_chats(self, user: UserResponse):
        return await self.repository.get_chats(user.id)

    async def update_chat(self, chat_id: int, chat: ChatUpdateDTO, user: UserResponse):
        return await self.repository.update_chat(chat_id, chat, user)

    async def delete_chat(self, chat_id: int, user: UserResponse):
        _deleted_chat = await self.repository.delete_chat(chat_id, user.id)
        if not _deleted_chat:
            raise HTTPException(404, "Chat not found")
        return _deleted_chat