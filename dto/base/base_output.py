import datetime
from pydantic import BaseModel


class BaseOutput(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime