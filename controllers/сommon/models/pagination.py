from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginationMeta(BaseModel):
    items_count: int
    page: int
    total_pages: int

class PaginatedResponse(BaseModel, Generic[T]):
    data: T
    meta: PaginationMeta