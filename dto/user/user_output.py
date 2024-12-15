from dto.base.base_output import BaseOutput


class UserOutput(BaseOutput):
    id: int
    name: str
    email: str
    password: str
    group_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
