from core.service import ServiceBase
from domain.group.group_domain import GroupDomain
from dto.base.pagination import (
    FilterBase,
    ListDomainResponse,
    PaginationResponse,
)
from sqlalchemy.orm import Session
from infrastructure.entities.group import GroupEntity
from infrastructure.repositories.group import GroupRepository
from dto.group.group_input import GroupInput


class GroupFactory:
    def __init__(self, service: "GroupService"):
        self.service = service

    def to_domain(self, entity: GroupEntity) -> "GroupDomain":
        return GroupDomain(entity, self.service.session)

    def to_domains(
        self, response: PaginationResponse[GroupEntity]
    ) -> ListDomainResponse["GroupDomain"]:
        return ListDomainResponse[GroupDomain](
            items=[self.to_domain(entity) for entity in response.items],
            total=response.total,
            page=response.page,
            limit=response.limit,
        )


class GroupService(ServiceBase):

    def __init__(self, session: Session):
        super().__init__(session)
        self.repository: GroupRepository = GroupRepository(session)

    def browse(self, filter: FilterBase) -> ListDomainResponse["GroupDomain"]:
        return GroupFactory(self).to_domains(self.repository.browse(filter))

    def read(self, id: int) -> GroupDomain:
        return GroupFactory(self).to_domain(self.repository.read(id))

    def edit(self, id: int, group: GroupInput) -> GroupDomain:
        return GroupFactory(self).to_domain(self.repository.edit(id, group))

    def add(self, data: GroupInput) -> GroupDomain:
        return GroupFactory(self).to_domain(self.repository.add(data))

    def delete(self, id: int) -> None:
        self.repository.delete(id)
