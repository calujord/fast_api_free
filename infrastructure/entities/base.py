import abc
from sqlalchemy import Column, DateTime, Integer
import datetime
from sqlalchemy.orm import declarative_base, declared_attr


Base = declarative_base()
class BaseEntity:
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
