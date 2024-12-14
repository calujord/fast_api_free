from domain.domain_base import BaseDomain
from fastapi import Depends

from dto.group.group_output import GroupOutput
from infrastructure.entities.group import GroupEntity

from domain.group.group_service import GroupService
from dto.base.pagination import FilterBase, OutputResponse
from dto.group.group_input import GroupInput
from dto.group.group_pick import GroupPick

class GroupDomain(BaseDomain):
    entity: GroupEntity
    service: GroupService = Depends(GroupService)

    def browse(self, filter: FilterBase) -> OutputResponse[GroupOutput]:
        response = self.service.browse(filter)
        return OutputResponse[GroupOutput](
            items=[GroupOutput.from_domain(item) for item in response.items],
            total=response.total,
            page=response.page,
            limit=filter.limit
        )
    
    def read(self, pick: GroupPick) -> GroupOutput:
        return self.service.read(pick).to_output()
    
    def edit(self, pick: GroupPick, data: GroupInput) -> GroupOutput:
        return self.service.edit(pick, data).to_output()
    
    def add(self, data: GroupInput) -> GroupOutput:
        return self.service.add(data).to_output()
    
    def delete(self, pick: GroupPick) -> None:
        return self.service.delete(pick)
    
    @classmethod
    def factory(cls, entity: GroupEntity) -> 'GroupDomain':
        return cls(
            entity=entity,
            service=GroupService()
        )
        
    def to_output(self) -> GroupOutput:
        return GroupOutput.from_domain(self)