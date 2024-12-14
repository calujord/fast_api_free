from typing import Optional, List
import pydantic
from typing import TypeVar, Generic
from typing import TypeVar

from dto.base.base_output import BaseOutput

T = TypeVar('T', bound='BaseEntity')
D = TypeVar('D', bound='BaseOutput')
BD = TypeVar('BD', bound='BaseDomain')
from domain.domain_base import BaseDomain
from infrastructure.entities.base import BaseEntity

class FilterBase(pydantic.BaseModel):
    page: int
    limit: int
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