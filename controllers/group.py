from fastapi import Depends
from core.controller import Controller
from domain.access_domain import AccessDomain
from dto.base.pagination import (
    FilterBase,
    OutputResponse,
)
from dto.group.group_input import GroupInput
from dto.group.group_output import GroupOutput
from dto.group.group_pick import GroupPick
from lib.decorator import api, get, post, put, tags, delete


@api("/group")
@tags(["Group"])
class Group(Controller):

    @get("/")
    async def browse(
        self, filter: FilterBase = Depends()
    ) -> OutputResponse[GroupOutput]:
        result = AccessDomain(session=self.session).group.browse(filter=filter)
        return OutputResponse[GroupOutput](
            items=[domain.entity for domain in result.items],
            total=result.total,
            page=result.page,
            limit=result.limit,
        )

    @get("/{id}")
    async def read(self, pick: GroupPick = Depends()) -> GroupOutput:
        return AccessDomain(session=self.session).group.read(pick.id).entity

    @put("/{id}")
    async def edit(
        self,
        data: GroupInput,
        pick: GroupPick = Depends(),
    ) -> GroupOutput:
        return (
            AccessDomain(
                session=self.session,
            )
            .group.edit(pick.id, data)
            .entity
        )

    @post("/")
    async def add(self, data: GroupInput) -> GroupOutput:
        return AccessDomain(session=self.session).group.add(data).entity

    @delete("/{id}")
    async def delete(self, pick: GroupPick) -> None:
        return AccessDomain(session=self.session).group.delete(pick.id)
