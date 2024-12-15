import pydantic


class GroupInput(pydantic.BaseModel):
    name: str = pydantic.Field(title="Group name")
    description: str = pydantic.Field(title="Group description")
