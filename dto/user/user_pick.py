import pydantic


class UserPick(pydantic.BaseModel):
    id: int
    group_id: int