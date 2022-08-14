from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type, Union, cast

from ..errors import Error
from ..models import AddedItem, Comparator, ListOrRef, SetError, StrOrRef
from ..serializer import Model


class MethodBase(Model):
    name = ""


class Method(MethodBase):
    using: set[str] = set()


@dataclass
class MethodWithAccount(Method):
    account_id: Optional[str] = field(init=False, default=None)


class ResponseCollector(MethodBase):
    response_types: Dict[str, Type[Union[Error, Response]]] = {}

    @classmethod
    def __init_subclass__(cls) -> None:
        if cls.name:
            ResponseCollector.response_types[cls.name] = cast(
                Type[Response], cls
            )


@dataclass
class Response(ResponseCollector):
    pass


@dataclass
class ResponseWithAccount(Response):
    account_id: Optional[str]


@dataclass
class InvocationBase:
    id: str


@dataclass
class Invocation(InvocationBase):
    method: Method


@dataclass
class InvocationResponseOrError(InvocationBase):
    response: Union[Error, Response]


@dataclass
class InvocationResponse(InvocationResponseOrError):
    response: Response


@dataclass
class Changes(MethodWithAccount):
    since_state: str
    max_changes: Optional[int] = None


@dataclass
class ChangesResponse(ResponseWithAccount):
    old_state: str
    new_state: str
    has_more_changes: bool
    created: List[str]
    updated: List[str]
    destroyed: List[str]


@dataclass
class Get(MethodWithAccount):
    ids: Optional[ListOrRef[str]]
    properties: Optional[List[str]] = None


@dataclass
class GetResponse(ResponseWithAccount):
    state: Optional[str]
    not_found: Optional[List[str]]


@dataclass
class Set(MethodWithAccount):
    if_in_state: Optional[StrOrRef] = None
    create: Optional[Dict[str, Any]] = None
    update: Optional[Dict[str, Dict[str, Any]]] = None
    destroy: Optional[ListOrRef] = None


@dataclass
class SetResponse(ResponseWithAccount):
    old_state: Optional[str]
    new_state: Optional[str]
    created: Optional[Dict[str, Any]]
    updated: Optional[Dict[str, Any]]
    destroyed: Optional[List[str]]
    not_created: Optional[Dict[str, SetError]]
    not_updated: Optional[Dict[str, SetError]]
    not_destroyed: Optional[Dict[str, SetError]]


@dataclass
class Query(MethodWithAccount):
    sort: Optional[List[Comparator]] = None
    position: Optional[int] = None
    anchor: Optional[str] = None
    anchorOffset: Optional[int] = None
    limit: Optional[int] = None
    calculateTotal: Optional[bool] = None


@dataclass
class QueryResponse(ResponseWithAccount):
    query_state: str
    can_calculate_changes: bool
    position: int
    ids: ListOrRef[str]
    total: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class QueryChanges(MethodWithAccount):
    sort: Optional[List[Comparator]] = None
    since_query_state: Optional[str] = None
    max_changes: Optional[int] = None
    up_to_id: Optional[str] = None
    calculate_total: bool = False


@dataclass
class QueryChangesResponse(ResponseWithAccount):
    old_query_state: str
    new_query_state: str
    removed: List[str]
    added: List[AddedItem]
    total: Optional[int] = None
