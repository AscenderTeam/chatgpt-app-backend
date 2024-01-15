# controllers/chat/models.py
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

class ChatCreateDTO(BaseModel):
    name: str
    vectorstore_path: str
    config: dict
    created_by_id: Optional[int] = Field(None, exclude=True)

    class Config:
        schema_extra = {
            "example": {
                "name": "Nombre del chat",
                "vectorstore_path": "ruta/a/tu/vectorstore",
                "config": {"param1": "valor1", "param2": "valor2"},
            }
        }

class ChatUpdateDTO(BaseModel):
    name: str
    vectorstore_path: Optional[str] = None
    config: Optional[dict] = None

class ChatResponse(BaseModel):
    id: int
    name: str
    vectorstore_path: str
    config: dict
    created_by_id: int
    created_at: datetime
    updated_at: datetime