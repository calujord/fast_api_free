from typing import Optional
import pydantic


class UserInput(pydantic.BaseModel):
    name: str = pydantic.Field(title="User name")
    email: str = pydantic.Field(title="User description")
    password: str = pydantic.Field(title="User password")
    group_id: int = pydantic.Field(title="User group id")
