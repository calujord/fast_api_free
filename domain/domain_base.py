import abc
from typing import Any, TypeVar
import pydantic

from infrastructure.entities.base import BaseEntity

T = TypeVar('T', bound='BaseEntity')

class BaseDomain(pydantic.BaseModel):
    entity: BaseEntity

    class Config:
        arbitrary_types_allowed = True
