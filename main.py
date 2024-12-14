from fastapi import Depends
from api.controllers.group import Group
from api.controllers.user import User
from app import MainApi
from domain.access_domain import AccessDomain
from dto.base.pagination import FilterBase




# create app instance
app = MainApi()
# add controllers
# app.add_controllers([
#     User,
#     Group
# ])

@app.get("/")
def read_root(filter: FilterBase = Depends()):
    access_domain = AccessDomain(session=app.session_local)
    return access_domain.service.browse(filter=filter)
