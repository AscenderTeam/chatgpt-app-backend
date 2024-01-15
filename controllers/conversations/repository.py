# from entities.[your_entity] import [YourEntity]Entity
from core.extensions.repositories import Repository
from entities.message import MessageEntity


class ConversationsRepo(Repository):
    messages: MessageEntity

    async def get_messages(self, chat_id: int):
        return await self.messages.filter(chat_id=chat_id).all()
