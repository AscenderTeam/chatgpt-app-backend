# controllers/chat/repository.py
from controllers.chats.models import ChatCreateDTO, ChatUpdateDTO
from core.extensions.authentication import AscenderAuthenticationFramework
from core.extensions.authentication.entity import UserEntity
from core.extensions.repositories import Repository
from entities.chat import ChatEntity

from tortoise.expressions import Q


class ChatRepo(Repository):

    def __init__(self) -> None:
        self.provider = AscenderAuthenticationFramework.auth_provider

    async def create_chat(self, chat_data: ChatCreateDTO, user_id: int):
        chat = await ChatEntity.create(**chat_data.model_dump(), created_by_id=user_id)
        await chat.fetch_related("invited_users", "created_by", "personality")
        return chat

    async def get_chat(self, chat_id: int, user_id: int):
        return await ChatEntity.get_or_none(Q(id=chat_id) & (Q(created_by_id=user_id) | Q(invited_users__id=user_id))).prefetch_related("invited_users", "created_by", "personality")

    async def get_chats(self, user_id: int):
        return await ChatEntity.filter(Q(created_by_id=user_id) | Q(invited_users__id=user_id)).prefetch_related("invited_users", "created_by", "personality").all()

    async def get_chats_offsetted(self, user_id: int, offset: int, page_size: int):
        return await ChatEntity.filter(Q(created_by_id=user_id) | Q(invited_users__id=user_id)).offset(offset).limit(page_size).prefetch_related("invited_users", "created_by", "personality").all()
    
    async def get_chats_count(self, user_id: int):
        return await ChatEntity.filter(Q(created_by_id=user_id) | Q(invited_users__id=user_id)).all().count()

    async def update_chat(self, chat_id: int, chat_data: ChatUpdateDTO):
        await ChatEntity.filter(id=chat_id).update(**chat_data.model_dump())
        return await self.get_chat(chat_id)

    async def delete_chat(self, chat_id: int, user_id: int):
        chat = await self.get_chat(chat_id, user_id=user_id)
        if chat:
            await chat.delete()
            
        return chat

    async def add_users_to_chat(self, chat_id: int, owner_id: int, *user_ids: int):
        chat = await self.get_chat(chat_id, user_id=owner_id)
        if not chat:
            return None

        invited_users: list[UserEntity] = []
        for user_id in user_ids:
            user = await self.provider.get_user(user_id)
            if not user:
                raise Exception("User not found")
            
            invited_users.append(user)

        await chat.invited_users.add(*invited_users)    
        
        return chat
    
    async def get_invited_chat(self, chat_id: int, user_id: int):
        return await ChatEntity.filter(id=chat_id, invited_users__id=user_id).prefetch_related("invited_users").all()

    async def get_invited_chats(self, user_id: int):
        return await ChatEntity.filter(invited_users__id=user_id).prefetch_related("invited_users").all()