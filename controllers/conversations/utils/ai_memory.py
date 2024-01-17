from controllers.conversations.repository import ConversationsRepo
from core.extensions.services import Service
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema.messages import ChatMessage

from entities.message import AuthorTypeEnum

class AIMemoryService(Service):
    def __init__(self, repository: ConversationsRepo) -> None:
        self._repository = repository
        
    async def get_messages(self, chat_id: int):
        _cbwm = ConversationBufferWindowMemory()
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