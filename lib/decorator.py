from fastapi import APIRouter
from functools import wraps

def api(path: str):
    def decorator(cls):
        cls.prefix = path
        cls.router = APIRouter()
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and hasattr(attr, "_path"):
                cls.router.add_api_route(attr._path, attr, methods=attr._methods)
        return cls
    return decorator

def route_decorator(method: str, path: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        wrapper._path = path
        wrapper._methods = [method]
        return wrapper
    return decorator

def get(path: str):
    return route_decorator("GET", path)

def post(path: str):
    return route_decorator("POST", path)

def put(path: str):
    return route_decorator("PUT", path)

def delete(path: str):
    return route_decorator("DELETE", path)

def tags(*tag_names: list[str]):
    def decorator(func):
        func._tags = tag_names
        return func
    return decorator