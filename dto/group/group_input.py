from typing import Optional
import pydantic


class GroupInput(pydantic.BaseModel):
    id: Optional[int] = pydantic.Field(default=None, title="Group ID")
    name: str = pydantic.Field(title="Group name")
    description: str = pydantic.Field(title="Group description")
    
    class Config:
        from_attributes = True