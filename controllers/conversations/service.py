from controllers.auth.models import UserResponse
from controllers.chats.endpoints import ChatController
from core.extensions.services import Service
from controllers.conversations.repository import ConversationsRepo
from core.utils.sockets import ApplicationContext


class ConversationsService(Service):

    chats: ChatController

    def __init__(self, repository: ConversationsRepo) -> None:
        self._repository = repository
    
    def __mounted__(self):
        """
        This method will be called when the service is mounted to the controller
        """
        self.inject_controller("ChatController", "chats")
    
    async def connect(self, ctx: ApplicationContext, user: UserResponse):
        await ctx.emit("status", "Successfully connected")
        
        chats = await self.chats.chat_service.get_chats(user)

         

    async def send_message(self, ctx: ApplicationContext, data: dict, user: UserResponse):
        pass
