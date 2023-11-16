from enum import Enum
from typing import Any, Sequence

from fastapi import APIRouter
from fastapi.datastructures import Default
from fastapi.params import Depends


class Controller:
    def __init__(self, tags: list[str] = [], prefix: str = "") -> None:
        self.prefix = prefix
        self.tags = tags

    def __call__(self, cls: object):
        router = APIRouter(tags=self.tags, prefix=self.prefix)
        
        def wrapper(*args, **kwargs):
            instance = cls(*args, **kwargs)
            
            for name, method in instance.__class__.__dict__.items():
                if hasattr(getattr(instance, name), "_controller_keyword_args") and hasattr(getattr(instance, name), "_controller_method"):
                    router.add_api_route(endpoint=getattr(instance, name), methods=[method._controller_method], **method._controller_keyword_args)

            instance.router = router
            return instance

        return wrapper


def Get(path: str = "/", response_model: Any = Default(None),
                 status_code: int | None = None,
                 tags: list[str | Enum] = None,
                 dependencies: Sequence[Depends] = [], **kwargs):

    if not path.startswith("/"):
        path = f"/{path}"

    def decorator(func):
        func._controller_keyword_args = {
            "path": path,
            "response_model": response_model,
            "status_code": status_code,
            "tags": tags,
            "dependencies": dependencies,
            **kwargs,
        }
        func._controller_method = "GET"
        return func

    return decorator

def Post(path: str = "/", response_model: Any = Default(None),
                 status_code: int | None = None,
                 tags: list[str | Enum] = None,
                 dependencies: Sequence[Depends] | None = None, **kwargs):
    
    if not path.startswith("/"):
        path = f"/{path}"

    def decorator(func):
        func._controller_keyword_args = {
            "path": path,
            "response_model": response_model,
            "status_code": status_code,
            "tags": tags,
            "dependencies": dependencies,
            **kwargs,
        }
        func._controller_method = "POST"
        return func

    return decorator

def Put(path: str = "/", response_model: Any = Default(None),
                 status_code: int | None = None,
                 tags: list[str | Enum] = None,
                 dependencies: Sequence[Depends] | None = None, **kwargs):
        
    if not path.startswith("/"):
        path = f"/{path}"

    def decorator(func):
        func._controller_keyword_args = {
            "path": path,
            "response_model": response_model,
            "status_code": status_code,
            "tags": tags,
            "dependencies": dependencies,
            **kwargs,
        }
        func._controller_method = "PUT"
        return func

    return decorator

def Patch(path: str = "/", response_model: Any = Default(None),
                 status_code: int | None = None,
                 tags: list[str | Enum] = None,
                 dependencies: Sequence[Depends] | None = None, **kwargs):
                
    if not path.startswith("/"):
        path = f"/{path}"
        
    def decorator(func):
        func._controller_keyword_args = {
            "path": path,
            "response_model": response_model,
            "status_code": status_code,
            "tags": tags,
            "dependencies": dependencies,
            **kwargs,
        }
        func._controller_method = "PATCH"
        return func

    return decorator

def Delete(path: str = "/", response_model: Any = Default(None),
                 status_code: int | None = None,
                 tags: list[str | Enum] = None,
                 dependencies: Sequence[Depends] | None = None, **kwargs):
            
    if not path.startswith("/"):
        path = f"/{path}"
            
    def decorator(func):
        func._controller_keyword_args = {
            "path": path,
            "response_model": response_model,
            "status_code": status_code,
            "tags": tags,
            "dependencies": dependencies,
            **kwargs,
        }
        func._controller_method = "DELETE"
        return func

    return decorator