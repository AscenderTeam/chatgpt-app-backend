from typing import Literal, Optional
from pydantic import BaseModel


class CompletionChoice(BaseModel):
    text: str
    index: int = 0
    logprobs: Optional[dict]
    finish_reason: Literal["length", "stop"]


class CompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResponse(BaseModel):
    id: str
    model: str = "mistral-7b-instruct"
    object: str = "text_completion"
    created: int
    choices: list[CompletionChoice]
    usage: CompletionUsage