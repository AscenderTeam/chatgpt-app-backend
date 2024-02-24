import asyncio
import json
from typing import AsyncIterator
from fastapi import HTTPException
from controllers.auth.models import UserResponse
from controllers.chats.endpoints import ChatController
from controllers.conversations.models import MessageDTO, PersonalityResponse
from controllers.conversations.serializers import MessageSerializer
from controllers.conversations.utils.ai_memory import AIMemoryService
from controllers.сommon.instructions.intro import INTRODUCTION_FOR_AI_GROUP, INTRODUCTION_FOR_AI_PRIVATE
from core.extensions.serializer import QuerySetSerializer, Serializer
from core.extensions.services import Service
from controllers.conversations.repository import ConversationsRepo
from core.utils.sockets import ApplicationContext
from entities.message import AuthorTypeEnum
from ascenderai import AscenderAI
from modules.cluster.types import CompletionResponse


class ConversationsService(Service):

    chats: ChatController

    def __init__(self, repository: ConversationsRepo) -> None:
        self._repository = repository
        self.llm = AscenderAI("ascender-7b-001", max_tokens=300, streaming=True, verbose=True)
        self.llm.base_url = "http://178.252.103.102:8000"
    
    def __mounted__(self):
        """
        This method will be called when the service is mounted to the controller
        """
        self.inject_controller("ChatController", "chats")
        self.ai_memory_service = AIMemoryService(self._repository)
    
    async def get_personalities(self, user: UserResponse):
        """
        Get personalities
        """
        personalities = await self._repository.get_personalities()

        return list(QuerySetSerializer.serialize_queryset(Serializer, PersonalityResponse, personalities))

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
            
        instruction = INTRODUCTION_FOR_AI_GROUP.format(users="".join([user.username] + [u.username for u in chat.invited_users])) if len(chat.invited_users) else INTRODUCTION_FOR_AI_PRIVATE.format(user=user.username)
        
        if chat.personality_id is not None:
            if chat.personality is None:
                await ctx.emit("error", {"code": 404, "details": "Personality not found"})
                return
            instruction = f"Name: {chat.personality.name}\nAppearance: {chat.personality.appearance}\nDescription: {chat.personality.description}\nRules: You are engaging in infinite roleplay mode with {user.username}, follow the dialogue line and do not add user's responses to your responses"
        
        messages = await self.ai_memory_service.get_messages(chat.id)
        
        try:
            response: AsyncIterator[CompletionResponse] = await self.llm.completions.create(f"""<s><|im_start|>system\n{instruction}<|im_end|>\n{self.ai_memory_service.convert_messages(messages.buffer_as_messages)}\n<|im_start|>assistant\nAI:""", stop_seqs=["<|im_end|>"])
        except asyncio.TimeoutError:
            await ctx.emit("error", {"code": 408, "details": "Streaming speed timed out"})
        await ctx.emit("stream_start", {"chat_id": chat.id}, room=f"chat_{chat.id}")
        complete = ""
        finish_reason = None
        async for chunk in response:
            await ctx.emit("stream_message", {
                "chat_id": chat.id,
                "content": chunk.choices[0].text,
            }, room=f"chat_{chat.id}")
            complete += chunk.choices[0].text
            finish_reason = chunk.choices[0].finish_reason

        generated_message = await self._repository.create_message(user.id, **MessageDTO(
            content=complete,
            chat_id=chat.id,
            author_type=AuthorTypeEnum.AI,
        ).model_dump())

        await ctx.emit("stream_end", {
            "chat_id": chat.id,
            "finish_reason": finish_reason,
            "message": json.loads(MessageSerializer(None, generated_message)().model_dump_json()),
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
        await ctx.emit("received_message", MessageSerializer(None, sent_message, author=user)(), room=f"chat_{chat.id}")