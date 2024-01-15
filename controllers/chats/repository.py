# controllers/chat/repository.py
from controllers.chats.models import ChatUpdateDTO
from core.extensions.authentication import AscenderAuthenticationFramework
from core.extensions.authentication.entity import UserEntity
from core.extensions.repositories import Repository
from entities.chat import ChatEntity


class ChatRepo(Repository):

    def __init__(self) -> None:
        self.provider = AscenderAuthenticationFramework.auth_provider

    async def create_chat(self, chat_data):
        chat = ChatEntity(**chat_data.dict())
        await chat.save()
        return chat

    async def get_chat(self, chat_id: int, user_id: int):
        return await ChatEntity.get_or_none(id=chat_id, user_id=user_id).prefetch_related("invited_users")

    async def get_chats(self, user_id: int):
        return await ChatEntity.filter(user_id=user_id).prefetch_related("invited_users").all()

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
    
    async def get_invited_chats(self, chat_id: int, user_id: int):
        return await ChatEntity.filter(id=chat_id, invited_users__id=user_id).prefetch_related("invited_users").all()