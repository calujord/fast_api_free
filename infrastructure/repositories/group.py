from dataclasses import dataclass
import datetime

from sqlalchemy.orm import Query
from dto.base.pagination import FilterBase, PaginationResponse
from dto.group.group_input import GroupInput
from infrastructure.entities.base import BaseEntity
from infrastructure.entities.group import GroupEntity
from sqlalchemy.orm import Session

from sqlalchemy import or_


class SuperQuery(Query):

    # override filter and only active
    def __get__(self, instance, owner):
        return Query.__get__(self, instance, owner).filter(
            BaseEntity.is_active,
        )


@dataclass
class GroupRepository:
    db: Session

    def browse(self, filter: FilterBase) -> PaginationResponse:
        query = self.db.query(GroupEntity)

        if filter.search:
            search = f"%{filter.search}%"
            query = query.filter(
                or_(
                    GroupEntity.name.ilike(search),
                    GroupEntity.description.ilike(search),
                ),
                GroupEntity.is_active,
                # active
            )

        total = query.count()

        if filter.page and filter.limit:
            query = query.offset(
                (filter.page - 1) * filter.limit,
            ).limit(filter.limit)

        groups = query.all()

        return PaginationResponse(
            items=groups, total=total, page=filter.page, limit=filter.limit
        )

    def read(self, id: int) -> GroupEntity:
        """
        Retrieve a group by its ID.
        Args:
            id (int): The ID of the group to retrieve.
        Returns:
            Group: The group object if found.
        Raises:
            ValueError: If no group with the specified ID is found.
        """

        group = (
            self.db.query(GroupEntity)
            .filter(
                GroupEntity.id == id,
                GroupEntity.is_active,
            )
            .first()
        )
        if group is None:
            raise ValueError(f"Group with id {id} not found")
        return group

    def edit(self, id: int, group: GroupInput) -> GroupEntity:
        """
        Edit an existing group with the provided data.
        Args:
            id (int): The ID of the group to be edited.
            group (dict): A dictionary containing the new data for the group.
                         Expected keys are "name" and "description".
        Returns:
            Group: The updated group object.
        """

        _group = (
            self.db.query(GroupEntity)
            .filter(
                GroupEntity.id == id,
            )
            .first()
        )
        if _group is None:
            raise ValueError(f"Group with id {id} not found")
        # update with group input

        self.db.query(GroupEntity).filter(GroupEntity.id == id).update(
            {k: v for k, v in group.model_dump().items()}
        )
        self.db.commit()
        return _group

    def add(self, input: GroupInput) -> GroupEntity:
        group_new = GroupEntity(**input.model_dump())
        self.db.add(group_new)
        self.db.commit()
        # Actualiza la instancia con el ID generado por la BD
        self.db.refresh(group_new)
        return group_new

    def delete(self, id: int) -> None:
        group = self.db.query(GroupEntity).filter(GroupEntity.id == id).first()
        if group is None:
            raise ValueError(f"Group with id {id} not found")
        # delete at the end of the session
        self.db.query(GroupEntity).filter(GroupEntity.id == id).update(
            {"deleted_at": datetime.datetime.now(), "is_active": False}
        )
        self.db.commit()
