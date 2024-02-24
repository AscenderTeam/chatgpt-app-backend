# controllers/chat/serializer.py
from controllers.auth.models import UserResponse
from controllers.conversations.models import PersonalityResponse
from core.extensions.serializer import Serializer
from controllers.chats.models import ChatResponse
from entities.chat import ChatEntity

class ChatSerializer(Serializer):
    def __init__(self, pd_model: object, entity: ChatEntity):
        self.pd_model = ChatResponse
        self.entity = entity
        self.values = {
            "invited_users": [Serializer(UserResponse, user)() for user in entity.invited_users] if entity.invited_users else [],
            "created_by": Serializer(UserResponse, entity.created_by)(),
            "personality": None if not entity.personality else Serializer(PersonalityResponse, entity.personality)(),
        }

    def serialize(self):
        return self.entity
