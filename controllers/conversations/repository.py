# from entities.[your_entity] import [YourEntity]Entity
from core.extensions.repositories import Repository
from entities.message import MessageEntity


class ConversationsRepo(Repository):
    messages: MessageEntity

    async def get_messages(self, chat_id: int, limit: int = 100):
        return await self.messages.filter(chat_id=chat_id).prefetch_related("user_author").all()

    async def create_message(self, user_id: int, **data):
        return await self.messages.create(user_author_id=user_id, **data)