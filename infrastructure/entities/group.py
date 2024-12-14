from sqlalchemy import Column, String
from infrastructure.entities.base import BaseEntity

class GroupEntity(BaseEntity):
    __tablename__ = 'groups'

    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self):
        return f"<Group(name={self.name}, description={self.description})>"
    
    class Config:
        from_attributes = True
        
        