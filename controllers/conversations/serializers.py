from typing import Any
from controllers.conversations.models import MessageResponse
from core.extensions.serializer import Serializer


class MessageSerializer(Serializer):
    def __init__(self, pd_model: Any, entity: type | None, **values) -> None:
        self.entity = entity
        self.pd_model = MessageResponse
        self.values = values
    
    def serialize(self):
        return self.entity