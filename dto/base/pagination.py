from typing import Optional, List
import pydantic
from typing import TypeVar, Generic

from dto.base.base_output import BaseOutput
from domain.domain_base import BaseDomain
from infrastructure.entities.base import BaseEntity


T = TypeVar("T", bound="BaseEntity")
D = TypeVar("D", bound="BaseOutput")
BD = TypeVar("BD", bound="BaseDomain")


class FilterBase(pydantic.BaseModel):
    page: int = pydantic.Field(1, description="Page number", example=1)
    limit: int = pydantic.Field(10, description="Items per page", example=10)
    search: Optional[str] = None


class PaginationBase(pydantic.BaseModel):
    page: int
    limit: int
    total: int

    class Config:
        arbitrary_types_allowed = True


class PaginationResponse(PaginationBase, Generic[T]):
    items: List[T]


class OutputResponse(PaginationBase, Generic[D]):
    items: List[D]


class ListDomainResponse(PaginationBase, Generic[BD]):
    items: List[BD]
