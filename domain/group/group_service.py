
from dto.base.pagination import FilterBase, ListDomainResponse
from sqlalchemy.orm import Session
from infrastructure.repositories.group import GroupRepository
from fastapi import Depends
from typing import TYPE_CHECKING
from dto.group.group_pick import GroupPick
from dto.group.group_input import GroupInput

# REMOVE CIRCULAR DEPENDENCY
if TYPE_CHECKING:
    from domain.group.group_domain import GroupDomain

class GroupService:
    def __init__(self, session: Session):
        self.repository: GroupRepository = GroupRepository(session)
    
    def browse(self, filter: FilterBase) -> ListDomainResponse['GroupDomain']:
        result = self.repository.browse(filter=filter)
        items = [GroupDomain.factory(item) for item in result.items]
        return ListDomainResponse[GroupDomain](items=items, total=result.total, page=filter.page, limit=filter.limit)
    
    def read(self, data: GroupPick) -> 'GroupDomain':
        return GroupDomain.factory(self.repository.read(data))
    
    def edit(self, data: GroupPick, group: GroupInput) -> 'GroupDomain':
        return GroupDomain.factory(self.repository.edit(data, group))
    
    def add(self, data: GroupInput) -> 'GroupDomain':
        return GroupDomain.factory(self.repository.add(data))
    
    def delete(self, data: GroupPick) -> None:
        return self.repository.delete(data)
    