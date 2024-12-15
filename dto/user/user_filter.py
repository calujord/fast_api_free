import pydantic
from dto.base.pagination import FilterBase


class UserFilter(FilterBase):
    group_id: int = pydantic.Field(title="Group ID")
