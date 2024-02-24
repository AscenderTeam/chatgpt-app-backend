from controllers.auth.models import UserResponse
from controllers.chats.endpoints import ChatController
from controllers.conversations.models import MessageResponse
from controllers.conversations.repository import ConversationsRepo
from controllers.conversations.serializers import MessageSerializer
from core.extensions.serializer import QuerySetSerializer, Serializer
from core.extensions.services import Service


class MessagesService(Service):

    chats: ChatController

    def __init__(self, repository: ConversationsRepo) -> None:
        self._repository = repository
    
    def __mounted__(self):
        """
        This method will be called when the service is mounted to the controller
        """
        print("Mounted called")
        self.inject_controller("ChatController", "chats")
    
    async def get_messages(self, chat_id: int, user: UserResponse,
                           page: int = 1, per_page: int = 20):
        chat = await self.chats.chat_service.get_chat(chat_id, user)
        
        messages_count = await self._repository.get_messages_count(chat.id)
        print(messages_count)
        messages = await self._repository.get_messages_offsetted(chat.id, (page - 1) * per_page, per_page)
        messages = list(QuerySetSerializer.serialize_queryset(
            MessageSerializer,
            MessageResponse,
            messages, 
            lambda m: {
                "author": Serializer(UserResponse, m.user_author)()
            }
        ))
        messages.reverse()
        return {
            "data": messages,
            "page": page,
            "total_pages": messages_count // per_page + 1
        }