from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, TypeVar, Union

from dataclasses_json import config

from ..ref import ResultReference
from ..serializer import Model

T = TypeVar("T")
StrOrRef = Union[str, ResultReference]
ListOrRef = Union[List[T], ResultReference]


@dataclass
class AddedItem(Model):
    id: str = field(metadata=config(field_name="Id"))
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
