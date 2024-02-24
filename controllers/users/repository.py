# from entities.[your_entity] import [YourEntity]Entity
from core.extensions.authentication.entity import UserEntity
from core.extensions.repositories import Repository


class UsersRepo(Repository):
    user: UserEntity

    async def get_users(self, limit: int):
        return await self.user.all().limit(limit)
    
    async def get_count(self, limit: int):
        return await self.user.all().count().limit(limit)