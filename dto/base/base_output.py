import datetime
from typing import Optional
from pydantic import BaseModel


class BaseOutput(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime] = None
    is_active: bool

    class Config:
        from_attributes = True
