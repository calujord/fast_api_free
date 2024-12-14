from typing import Optional
from fastapi import APIRouter
from sqlalchemy.orm import Session

class Controller:
    router = APIRouter()
    prefix: Optional[str] = None
    tags: list[str] = []
    session: Session
