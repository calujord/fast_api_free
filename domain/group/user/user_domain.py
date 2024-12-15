from domain.domain_base import BaseDomain
from sqlalchemy.orm import Session
from infrastructure.entities.user import UserEntity


class UserDomain(BaseDomain):
    entity: UserEntity

    def __init__(self, entity: UserEntity, session: Session) -> None:
        from domain.group.user.user_service import UserService

        self.entity = entity
        self.service = UserService(session=session)
