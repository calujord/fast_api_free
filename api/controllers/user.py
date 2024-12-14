
from api.controllers.base import Controller
from lib.decorator import api, get, post, put, tags, delete


@api("/user")
@tags(["User"])
class User(Controller):
    
    @get("/")
    async def browse(self):
        return {"message": "User browse"}
    
    @get("/{id}")
    async def read(self, id: int):
        return {"message": "User read"}
    
    @put("/{id}")
    async def edit(self, id: int):
        return {"message": "User edit"}
    
    @post("/")
    async def add(self):
        return {"message": "User add"}
    
    @delete("/{id}")
    async def delete(self, id: int):
        return {"message": "User delete"}