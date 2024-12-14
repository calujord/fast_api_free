from domain.group import group_domain as domain
from dto.base.base_output import BaseOutput

class GroupOutput(BaseOutput):
    id: int
    name: str
    
    @staticmethod
    def from_domain(group) -> 'GroupOutput':
        return GroupOutput(
            id=group.entity.id.value,
            name=group.entity.name.value,
            created_at=group.entity.created_at.value,
            updated_at=group.entity.updated_at.value,
            deleted_at=group.entity.deleted_at.value
        )
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True