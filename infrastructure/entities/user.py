from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from infrastructure.entities.base import BaseEntity

class User(BaseEntity):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"