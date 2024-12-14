from sqlalchemy import Column, ForeignKey, Integer, String
from infrastructure.entities.base import BaseEntity
from infrastructure.database.settings import BaseModelEntity

class UserEntity(BaseModelEntity, BaseEntity):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    
    
    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"