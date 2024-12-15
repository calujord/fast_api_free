from fastapi import Depends
from core.controller import Controller
from domain.access_domain import AccessDomain
from dto.base.pagination import OutputResponse
from dto.user.user_filter import UserFilter
from dto.user.user_input import UserInput
from dto.user.user_output import UserOutput
from dto.user.user_pick import UserPick
from lib.decorator import api, get, post, put, tags, delete


@api("/user")
@tags(["User"])
class User(Controller):

    @get("/")
    async def browse(
        self, filter: UserFilter = Depends()
    ) -> OutputResponse[UserOutput]:
        result = (
            AccessDomain(session=self.session)
            .group.read(filter.group_id)
            .user.browse(filter)
        )
        return OutputResponse[UserOutput](
            items=[domain.entity for domain in result.items],
            total=result.total,
            page=result.page,
            limit=result.limit,
        )

    @get("/{id}")
    async def read(self, pick: UserPick = Depends()) -> UserOutput:
        return (
            AccessDomain(session=self.session)
            .group.read(
                pick.group_id,
            )
            .entity
        )

    @put("/{id}")
    async def edit(self, id: int, data: UserInput) -> UserOutput:
        return (
            AccessDomain(session=self.session)
            .group.read(data.group_id)
            .user.edit(id, data)
            .entity
        )

    @post("/")
    async def add(self, data: UserInput) -> UserOutput:
        return (
            AccessDomain(session=self.session)
            .group.read(data.group_id)
            .user.add(data)
            .entity
        )

    @delete("/{id}")
    async def delete(self, pick: UserPick = Depends()) -> None:
        return (
            AccessDomain(session=self.session)
            .group.read(pick.group_id)
            .user.delete(pick.id)
        )
