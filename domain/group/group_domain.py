from dataclasses import dataclass
from typing import TYPE_CHECKING
from domain.domain_base import BaseDomain
from sqlalchemy.orm import Session
from domain.group.user.user_service import UserService
from infrastructure.entities.group import GroupEntity




class GroupDomain(BaseDomain):
    entity: GroupEntity
    
    def __init__(self, entity: GroupEntity, session: Session) -> None:
        from domain.group.group_service import GroupService
        self.entity = entity
        self.service = GroupService(session=session)
        self.user = UserService(session=session)