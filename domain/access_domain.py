from domain.group.group_service import GroupService

# session
from sqlalchemy.orm import Session

from domain.group.user.user_service import UserService


class AccessDomain:

    def __init__(self, session: Session):
        self.group = GroupService(session=session)
        self.user = UserService(session=session)
