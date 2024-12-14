from typing import Optional, Type
from fastapi import APIRouter
from sqlalchemy.orm import Session

class Controller:
    router = APIRouter()
    prefix: Optional[str] = None
    tags: list[str] = []
    session: Session

    def _register_routes(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, "_path"):
                method = getattr(self.router, attr._methods[0].lower())
                method(attr._path)(attr)
                