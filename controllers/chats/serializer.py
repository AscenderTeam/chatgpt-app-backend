# controllers/chat/serializer.py
from core.extensions.serializer import Serializer
from controllers.chats.models import ChatResponse

class ChatSerializer(Serializer):
    def __init__(self, entity):
        self.pd_model = ChatResponse
        self.entity = entity

    def serialize(self):
        return self.entity
