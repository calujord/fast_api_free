from dto.base.pagination import FilterBase, PaginationResponse
from dto.group.group_input import GroupInput
from dto.group.group_pick import GroupPick
from infrastructure.entities.group import GroupEntity
from sqlalchemy.orm import Session

from sqlalchemy import or_

class GroupRepository:
    def __init__(self, session: Session):
        self.session = session

    def browse(self, filter: FilterBase) -> PaginationResponse[GroupEntity]:
        query = self.session.query(GroupEntity)

        if filter.search:
            search = f"%{filter.search}%"
            query = query.filter(or_(GroupEntity.name.ilike(search), GroupEntity.description.ilike(search)))

        total = query.count()

        if filter.page and filter.limit:
            query = query.offset((filter.page - 1) * filter.limit).limit(filter.limit)

        groups = query.all()

        return PaginationResponse(
            items=groups,
            total=total,
            page=filter.page,
            limit=filter.limit
        )
    
    def read(self, data: GroupPick) -> GroupEntity:
        """
        Retrieve a group by its ID.
        Args:
            id (int): The ID of the group to retrieve.
        Returns:
            Group: The group object if found.
        Raises:
            ValueError: If no group with the specified ID is found.
        """
        
        group = self.session.query(GroupEntity).filter(GroupEntity.id == data.id).first()
        if group is None:
            raise ValueError(f"Group with id {data.id} not found")
        return group

    def edit(self, data: GroupPick, group: GroupInput) -> GroupEntity:
        """
        Edit an existing group with the provided data.
        Args:
            id (int): The ID of the group to be edited.
            group (dict): A dictionary containing the new data for the group. 
                         Expected keys are "name" and "description".
        Returns:
            Group: The updated group object.
        """
        
        _group = self.session.query(GroupEntity).filter(GroupEntity.id == data.id).first()
        if _group is None:
            raise ValueError(f"Group with id {data.id} not found")
        # update with group input
        self.session.commit()
        return _group
    
    def add(self, input: GroupInput) -> GroupEntity:
        self.session.add(input)
        self.session.commit()
        return self.read(data=GroupPick(id=input.id))
    
    def delete(self, data: GroupPick) -> None:
        group = self.session.query(GroupEntity).filter(GroupEntity.id == data.id).first()
        self.session.delete(group)
        self.session.commit()