from sqlalchemy import Boolean, Column, DateTime, Integer
import datetime
from sqlalchemy.orm import declared_attr


class BaseEntity:
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, default=None)
    is_active = Column(Boolean, default=True)

    def delete(self):
        self.deleted_at = datetime.datetime.utcnow()
        self.is_active = False
