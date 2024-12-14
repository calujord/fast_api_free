import pydantic
from dto.base.pagination import FilterBase
from typing import Optional


class UserFilter(FilterBase):
    group_id: int = pydantic.Field(title='Group ID')