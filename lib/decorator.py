from fastapi import APIRouter
from functools import wraps

def api(path: str):
    def decorator(cls):
        cls.prefix = path
        cls.router = APIRouter()
        #for attr_name in dir(cls):
        #    attr = getattr(cls, attr_name)
        #    cls.router.add_api_route(attr._path, attr, methods=attr._methods)
        #    if callable(attr) and hasattr(attr, "_path"):
        return cls
    return decorator


def get(path: str):
    def decorator(func):
        func._path = path
        func._methods = ["GET"]
        return func
    return decorator
    

def post(path: str):
    def decorator(func):
        func._path = path
        func._methods = ["POST"]
        return func
    return decorator

def put(path: str):
    def decorator(func):
        func._path = path
        func._methods = ["PUT"]
        return func
    return decorator

def delete(path: str):
    def decorator(func):
        func._path = path
        func._methods = ["DELETE"]
        return func
    return decorator

def tags(*tag_names: list[str]):
    def decorator(func):
        func.tags = tag_names
        return func
    return decorator