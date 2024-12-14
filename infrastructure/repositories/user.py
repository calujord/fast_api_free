from dataclasses import dataclass
import datetime

from dto.base.pagination import PaginationResponse
from dto.user.user_filter import UserFilter
from dto.user.user_input import UserInput
from infrastructure.entities.user import UserEntity
from sqlalchemy.orm import Session

from sqlalchemy import or_

@dataclass
class UserRepository:
    db: Session
    
    def browse(self, filter: UserFilter) -> PaginationResponse:
        query = self.db.query(UserEntity)

        if filter.search:
            search = f"%{filter.search}%"
            query = query.filter(
                or_(
                    UserEntity.name.ilike(search),
                    UserEntity.email.ilike(search),
                ),
                UserEntity.deleted_at == None,
                UserEntity.group_id == filter.group_id
            )

        total = query.count()

        if filter.page and filter.limit:
            query = query.offset((filter.page - 1) * filter.limit).limit(filter.limit)

        users = query.all()

        return PaginationResponse(
            items=users,
            total=total,
            page=filter.page,
            limit=filter.limit
        )
    
    def read(self, id: int) -> UserEntity:
        """
        Retrieve a user by its ID.
        Args:
            id (int): The ID of the user to retrieve.
        Returns:
            User: The user object if found.
        Raises:
            ValueError: If no user with the specified ID is found.
        """
        
        user = self.db.query(UserEntity).filter(UserEntity.id == id, UserEntity.deleted_at == None).first()
        if user is None:
            raise ValueError(f"User with id {id} not found")
        return user

    def edit(self, id: int, user: UserInput) -> UserEntity:
        """
        Edit an existing user with the provided data.
        Args:
            id (int): The ID of the user to be edited.
            user (dict): A dictionary containing the new data for the user. 
                         Expected keys are "name" and "description".
        Returns:
            User: The updated user object.
        """
        
        _user = self.db.query(UserEntity).filter(UserEntity.id == id).first()
        if _user is None:
            raise ValueError(f"User with id {id} not found")
        # update with user input
        
        self.db.query(UserEntity).filter(UserEntity.id == id).update({k: v for k, v in user.model_dump().items()})
        self.db.commit()
        return _user
    
    def add(self, input: UserInput) -> UserEntity:
        user_new = UserEntity(**input.model_dump())
        self.db.add(user_new)
        self.db.commit()
        # Actualiza la instancia con el ID generado por la BD
        self.db.refresh(user_new)  
        return user_new
    
    def delete(self, id: int) -> None:
        user = self.db.query(UserEntity).filter(UserEntity.id == id).first()
        if user is None:
            raise ValueError(f"User with id {id} not found")
        # delete at the end of the session
        self.db.query(UserEntity).filter(UserEntity.id == id).update({"deleted_at": datetime.datetime.now()})
        self.db.commit()