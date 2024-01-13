from core.extensions.services import Service
from controllers.chats.repository import ChatRepo
from controllers.chats.models import ChatCreateDTO, ChatUpdateDTO

class ChatService(Service):
    def __init__(self, repository: ChatRepo):
        self.repository = repository

    async def create_chat(self, chat: ChatCreateDTO):
        return await self.repository.create_chat(chat)

    async def get_chat(self, chat_id: int):
        return await self.repository.get_chat(chat_id)

    async def update_chat(self, chat_id: int, chat: ChatUpdateDTO):
        return await self.repository.update_chat(chat_id, chat)

    async def delete_chat(self, chat_id: int):
        return await self.repository.delete_chat(chat_id)