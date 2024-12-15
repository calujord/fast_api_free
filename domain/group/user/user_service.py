from core.service import ServiceBase
from domain.group.user.user_domain import UserDomain
from dto.base.pagination import ListDomainResponse, PaginationResponse
from sqlalchemy.orm import Session
from dto.user.user_filter import UserFilter
from infrastructure.entities.user import UserEntity
from dto.user.user_input import UserInput
from infrastructure.repositories.user import UserRepository


class UserFactory:
    def __init__(self, service: "UserService"):
        self.service = service

    def to_domain(self, entity: UserEntity) -> "UserDomain":
        return UserDomain(entity, self.service.session)

    def to_domains(
        self, response: PaginationResponse[UserEntity]
    ) -> ListDomainResponse["UserDomain"]:
        return ListDomainResponse[UserDomain](
            items=[self.to_domain(entity) for entity in response.items],
            total=response.total,
            page=response.page,
            limit=response.limit,
        )


class UserService(ServiceBase):

    def __init__(self, session: Session):
        super().__init__(session)
        self.repository: UserRepository = UserRepository(session)

    def browse(self, filter: UserFilter) -> ListDomainResponse["UserDomain"]:
        return UserFactory(self).to_domains(self.repository.browse(filter))

    def read(self, id: int) -> UserDomain:
        return UserFactory(self).to_domain(self.repository.read(id))

    def edit(self, id: int, user: UserInput) -> UserDomain:
        return UserFactory(self).to_domain(self.repository.edit(id, user))

    def add(self, data: UserInput) -> UserDomain:
        return UserFactory(self).to_domain(self.repository.add(data))

    def delete(self, id: int) -> None:
        self.repository.delete(id)
