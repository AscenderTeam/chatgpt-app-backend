# controllers/chat/repository.py
from core.extensions.repositories import Repository
from entities.chat import ChatEntity


class ChatRepo(Repository):
    async def create_chat(self, chat_data):
        chat = ChatEntity(**chat_data.dict())
        await chat.save()
        return chat

    async def get_chat(self, chat_id):
        return await ChatEntity.get(id=chat_id)

    async def update_chat(self, chat_id, chat_data):
        await ChatEntity.filter(id=chat_id).update(**chat_data.dict())
        return await self.get_chat(chat_id)

    async def delete_chat(self, chat_id):
        chat = await self.get_chat(chat_id)
        await chat.delete()
        return chat
