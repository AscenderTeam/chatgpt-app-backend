# from entities.[your_entity] import [YourEntity]Entity
from core.extensions.repositories import Repository
from entities.chat import PersonalityEntity
from entities.message import MessageEntity


class ConversationsRepo(Repository):
    messages: MessageEntity
    personality: PersonalityEntity

    async def get_messages(self, chat_id: int, limit: int = 100):
        return await self.messages.filter(chat_id=chat_id).prefetch_related("user_author").all()

    async def get_messages_offsetted(self, chat_id: int, offset: int = 0, limit: int = 100):
        return await self.messages.filter(chat_id=chat_id).offset(offset).limit(limit).prefetch_related("user_author").all().order_by("-id")

    async def get_messages_count(self, chat_id: int):
        return await self.messages.filter(chat_id=chat_id).count()

    async def create_message(self, user_id: int, **data):
        return await self.messages.create(user_author_id=user_id, **data)
    
    async def create_persona(self, **data):
        return await self.personality.create(**data)
    
    async def get_personalities(self):
        return await self.personality.all()