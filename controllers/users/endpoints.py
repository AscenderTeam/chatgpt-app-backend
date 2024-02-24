
from fastapi import Depends
from controllers.users.repository import UsersRepo
from controllers.users.service import UsersService
from core.extensions.authentication.entity import UserEntity
from core.guards.authenticator import IsAuthenticated
from core.types import ControllerModule
from core.utils.controller import Controller, Get

@Controller()
class Users:
    def __init__(self, users_service: UsersService) -> None:
        self.users_service = users_service

    @Get(
        dependencies=[
            Depends(IsAuthenticated())
        ]
    )
    async def get_users_endpoint(self, limit: int = 100):
        return await self.users_service.get_users(limit)


def setup() -> ControllerModule:
    return {
        "controller": Users,
        "services": {
            "users": UsersService
        },
        "repository": UsersRepo,
        "repository_entities": {
            "user": UserEntity
        }
    }