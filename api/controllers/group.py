
from fastapi import Depends, Query
from api.controllers.base import Controller
from domain.access_domain import AccessDomain
from dto.base.pagination import FilterBase
from lib.decorator import api, get, post, put, tags, delete

@api("/group")
@tags(["Group"])
class Group(Controller):
    
    @get("/")
    async def browse(self, filter: FilterBase = Depends()):
        access_domain = AccessDomain(session=self.session)
        items = access_domain.service.browse(filter=filter)
        return items.items
    
    @get("/{id}")
    async def read(self, id: int):
        return {"message": "Group read"}
    
    @put("/{id}")
    async def edit(self, id: int):
        return {"message": "Group edit"}
    
    @post("/")
    async def add(self):
        return {"message": "Group add"}
    
    @delete("/{id}")
    async def delete(self, id: int):
        return {"message": "Group delete"}