from dto.base.base_output import BaseOutput
from infrastructure.entities.user import UserEntity

class UserOutput(BaseOutput):
    id: int
    name: str
    email: str
    password: str
    group_id: int
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        
    @classmethod
    def from_orm(cls, entity: UserEntity) -> 'UserOutput':
        return cls(
            id=entity.id,  # type: ignore
            name=entity.name,  # type: ignore
            email=entity.email,  # type: ignore
            password=entity.password,  # type: ignore
            group_id=entity.group_id,  # type: ignore
            created_at=entity.created_at,  # type: ignore
            updated_at=entity.updated_at,  # type: ignore
            deleted_at=entity.deleted_at  # type: ignore
        )