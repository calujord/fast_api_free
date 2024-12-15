from typing import TypeVar

from infrastructure.entities.base import BaseEntity

T = TypeVar("T", bound="BaseEntity")


class BaseDomain:
    entity: BaseEntity
