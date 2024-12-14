from dto.base.base_output import BaseOutput

class GroupOutput(BaseOutput):
    id: int
    name: str
    description: str
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True