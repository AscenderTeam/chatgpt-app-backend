from fastapi import HTTPException
from pydantic import ValidationError
from controllers.auth.models import UserResponse
from controllers.chats.endpoints import ChatController
from controllers.conversations.models import MessageDTO
from controllers.conversations.serializers import MessageSerializer
from controllers.conversations.utils.ai_memory import AIMemoryService
from core.extensions.services import Service
from controllers.conversations.repository import ConversationsRepo
from core.utils.sockets import ApplicationContext
from entities.message import AuthorTypeEnum
from modules.cluster.ascender_ai import AscenderAIChat


class ConversationsService(Service):

    chats: ChatController

    def __init__(self, repository: ConversationsRepo) -> None:
        self._repository = repository
        self.llm = AscenderAIChat("mixtral-8x7b", max_tokens=500, streaming=True, verbose=True)
    
    def __mounted__(self):
        """
        This method will be called when the service is mounted to the controller
        """
        self.inject_controller("ChatController", "chats")
        self.ai_memory_service = AIMemoryService(self._repository)
    
    async def connect(self, ctx: ApplicationContext, user: UserResponse):
        await ctx.emit("status", "Successfully connected")
        
        chats = await self.chats.chat_service.get_chats(user)
        invited_chats = await self.chats.chat_service.get_invited_chats(user)

        for chat in chats:
            await ctx.enter_room(f"chat_{chat.id}")
        
        for chat in invited_chats:
            await ctx.enter_room(f"chat_{chat.id}")
        
    async def generate_ai_response(self, ctx: ApplicationContext, chat_id: int, user: UserResponse):
        """
        Generate AI response
        """
        try:
            chat = await self.chats.chat_service.get_chat(chat_id, user)
        except HTTPException as e:
            await ctx.emit("error", {"code": e.status_code, "details": e.detail})
            return

        messages = await self.ai_memory_service.get_messages(chat.id)
        response = await self.llm.get_completion(f"""{messages.buffer_as_str}\nAI:""", stop_seqs=[f"\n{user.username}:"])

        await ctx.emit("stream_start", {"chat_id": chat.id}, room=f"chat_{chat.id}")
        complete = ""
        async for chunk in response:
            await ctx.emit("received_message", chunk["choices"][0]["text"], room=f"chat_{chat.id}")
            complete += chunk["choices"][0]["text"]

        generated_message = await self._repository.create_message(user.id, **MessageDTO(
            content=complete,
            chat_id=chat.id,
            author_type=AuthorTypeEnum.AI,
        ).model_dump())

        await ctx.emit("stream_end", {
            "chat_id": chat.id,
            "message": MessageSerializer(generated_message)().model_dump_json(),
        }, room=f"chat_{chat.id}")

    async def send_message(self, ctx: ApplicationContext, data: MessageDTO, user: UserResponse):
        """
        Send message to the chat
        """

        try:
            chat = await self.chats.chat_service.get_chat(data.chat_id, user)
        except HTTPException as e:
            await ctx.emit("error", {"code": e.status_code, "details": e.detail})
            return

        sent_message = await self._repository.create_message(user.id, **data.model_dump())
        await ctx.emit("received_message", MessageSerializer(sent_message)(), room=f"chat_{chat.id}")