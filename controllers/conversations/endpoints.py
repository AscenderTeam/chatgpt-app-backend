from fastapi import Depends
from pydantic import ValidationError
from controllers.auth.models import UserResponse
from controllers.conversations.models import MessageDTO
from controllers.conversations.repository import ConversationsRepo
from controllers.conversations.service import ConversationsService
from controllers.conversations.services.messages import MessagesService
from core.extensions.authentication.entity import UserEntity
from core.extensions.serializer import Serializer
from core.guards.authenticator import GetAuthenticatedSocket, GetAuthenticatedUser, IsAuthenticated
from core.types import ControllerModule
from core.utils.controller import Controller, Get
from core.utils.sockets import ApplicationContext, Listen
from entities.chat import PersonalityEntity
from entities.message import MessageEntity

@Controller()
class Conversations:
    def __init__(self, conversations_service: ConversationsService,
                 messages_service: MessagesService) -> None:
        self.conversations_service = conversations_service
        self.messages_service = messages_service

        self.injectable_services = [conversations_service, messages_service]

    @Get("{chat_id}/messages")
    async def get_messages(self, chat_id: int, page: int = 1, per_parge: int = 20, user: UserEntity = Depends(GetAuthenticatedUser(True))):
        return await self.messages_service.get_messages(chat_id, user, page, per_parge)

    @Listen("connect")
    @GetAuthenticatedSocket(True)
    async def connect(self, ctx: ApplicationContext, user: UserEntity):
        user = Serializer(UserResponse, user)()
        return await self.conversations_service.connect(ctx, user=user)

    @Listen("generate_ai_response")
    @GetAuthenticatedSocket()
    async def generate_ai_response(self, ctx: ApplicationContext, user: UserEntity, 
                                   data: int):
        user = Serializer(UserResponse, user)()
        await self.conversations_service.generate_ai_response(ctx, chat_id=data, user=user)

    @Listen("send_message")
    @GetAuthenticatedSocket()
    async def send_message(self, ctx: ApplicationContext, user: UserEntity, 
                           data: dict):
        user = Serializer(UserResponse, user)()
        try:
            data = MessageDTO.model_validate(data)
        except ValidationError as e:
            await ctx.emit("error", e.json())
            return
        # print(data)
        await self.conversations_service.send_message(ctx, data=data, user=user)



def setup() -> ControllerModule:
    return {
        "controller": Conversations,
        "services": {
            "conversations": ConversationsService,
            "messages": MessagesService,
        },
        "repository": ConversationsRepo,
        "repository_entities": {
            "messages": MessageEntity,
            "personality": PersonalityEntity,
        }
    }
