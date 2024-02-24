from core.extensions.services import Service
from controllers.users.repository import UsersRepo
from core.extensions.authentication import AscenderAuthenticationFramework


class UsersService(Service):

    def __init__(self, repository: UsersRepo) -> None:
        self._repository = repository
        self.auth_provider = AscenderAuthenticationFramework.auth_provider

    
    async def get_users(self, limit: int = 100):
        return await self._repository.get_users(limit)

    async def get_user(self, user_id: int):
        return await self.auth_provider.get_user(user_id)