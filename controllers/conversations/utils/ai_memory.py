from typing import Optional
from controllers.conversations.repository import ConversationsRepo
from core.extensions.services import Service
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema.messages import ChatMessage, BaseMessage, AIMessage

from entities.message import AuthorTypeEnum

class AIMemoryService(Service):
    def __init__(self, repository: ConversationsRepo) -> None:
        self._repository = repository
        
    async def get_messages(self, chat_id: int):
        _cbwm = ConversationBufferWindowMemory(k=3, return_messages=True)
        messages = await self._repository.get_messages(chat_id)

        for message in messages:
            if message.author_type == AuthorTypeEnum.AI:
                _cbwm.chat_memory.add_ai_message(message.content)
            if message.author_type == AuthorTypeEnum.USER:
                _cbwm.chat_memory.add_message(ChatMessage(
                    content=message.content,
                    role=message.user_author.username
                ))
        
        return _cbwm
    
    def convert_messages(self, messages: list[BaseMessage]):
        response_string = ""
        for message in messages:
            if isinstance(message, AIMessage):
                response_string += f"<|im_start|>assistant\nAI: {message.content}<|im_end|>"
            elif isinstance(message, ChatMessage):
                response_string += f"<|im_start|>user\n{message.role}: {message.content}<|im_end|>"
            
        return response_string