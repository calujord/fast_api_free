from sqlalchemy import Column, String
from infrastructure.entities.base import BaseEntity
from infrastructure.database.settings import BaseModelEntity
class GroupEntity(BaseModelEntity, BaseEntity):
    __tablename__ = 'groups'

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    
    class Config:
        from_attributes = True
        
        
    def __repr__(self):
        return f"<Group(name={self.name}, description={self.description})>"