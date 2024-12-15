from domain.group.group_service import GroupService

# session
from sqlalchemy.orm import Session


class AccessDomain:

    def __init__(self, session: Session):
        self.group = GroupService(session=session)
