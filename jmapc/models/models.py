from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, TypeVar, Union

from dataclasses_json import config

from ..ref import Ref, ResultReference
from ..serializer import Model

T = TypeVar("T")
StrOrRef = Union[str, ResultReference, Ref]
ListOrRef = Union[list[T], ResultReference, Ref]
TypeOrRef = Union[T, ResultReference, Ref]


@dataclass
class Blob(Model):
    id: str = field(metadata=config(field_name="blobId"))
    type: str
    size: int


@dataclass
class AddedItem(Model):
    id: str = field(metadata=config(field_name="id"))
    index: int


@dataclass
class EmailAddress(Model):
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class Comparator(Model):
    property: str
    is_ascending: bool = True
    collation: Optional[str] = None
    anchor: Optional[str] = None
    anchor_offset: int = 0
    limit: Optional[int] = None
    calculate_total: bool = False
    position: int = 0


@dataclass
class FilterOperator(Model):
    operator: Operator


class Operator(Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


@dataclass
class SetError(Model):
    type: str
    description: Optional[str] = None
    already_exists: Optional[str] = None
    not_found: Optional[list[str]] = None
    properties: Optional[list[str]] = None
