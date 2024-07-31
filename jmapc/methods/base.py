from __future__ import annotations

import contextlib
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from typing import Set as SetType
from typing import Type, Union, cast

from ..errors import Error
from ..models import AddedItem, Comparator, ListOrRef, SetError, StrOrRef
from ..serializer import Model, null_omitted_field


class MethodBase(Model):
    using: SetType[str] = set()
    method_namespace: Optional[str] = None

    @property
    def jmap_method_name(self) -> str:
        return getattr(self, "jmap_method", None) or self.get_method_name()

    @classmethod
    def get_method_name(cls) -> str:
        if not cls.method_namespace:
            raise ValueError(f"Method {cls.__class__} has no method namespace")
        method_type = getattr(cls, "method_type", None)
        if not method_type:
            raise ValueError(f"Method {cls.__class__} has no method type")
        return f"{cls.method_namespace}/{method_type}"


class Method(MethodBase):
    pass


@dataclass
class MethodWithAccount(Method):
    account_id: Optional[str] = null_omitted_field(init=False)


class ResponseCollector(MethodBase):
    response_types: Dict[str, Type[Union[Error, Response]]] = {}

    @classmethod
    def __init_subclass__(cls) -> None:
        with contextlib.suppress(ValueError):
            method_name = cls.get_method_name()
            ResponseCollector.response_types[method_name] = cast(
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


class ChangesMethod:
    method_type: Optional[str] = "changes"


@dataclass
class Changes(MethodWithAccount, ChangesMethod):
    since_state: str
    max_changes: Optional[int] = null_omitted_field()


@dataclass
class ChangesResponse(ResponseWithAccount, ChangesMethod):
    old_state: str
    new_state: str
    has_more_changes: bool
    created: List[str]
    updated: List[str]
    destroyed: List[str]


class CopyMethod:
    method_type: Optional[str] = "copy"


@dataclass
class Copy(MethodWithAccount, CopyMethod):
    from_account_id: str
    if_from_in_state: Optional[str] = null_omitted_field()
    if_in_state: Optional[str] = null_omitted_field()
    on_success_destroy_original: bool = False
    destroy_from_if_in_state: Optional[str] = null_omitted_field()


@dataclass
class CopyResponse(ResponseWithAccount, CopyMethod):
    from_account_id: str
    old_state: str
    new_state: str
    not_created: Optional[Dict[str, SetError]]


class GetMethod:
    method_type: Optional[str] = "get"


@dataclass
class Get(MethodWithAccount, GetMethod):
    ids: Optional[ListOrRef[str]] = null_omitted_field()
    properties: Optional[List[str]] = null_omitted_field()


@dataclass
class GetResponseWithoutState(ResponseWithAccount, GetMethod):
    not_found: Optional[List[str]]


@dataclass
class GetResponse(GetResponseWithoutState):
    state: Optional[str]


class SetMethod:
    method_type: Optional[str] = "set"


@dataclass
class Set(MethodWithAccount, SetMethod):
    if_in_state: Optional[StrOrRef] = null_omitted_field()
    create: Optional[Dict[str, Any]] = null_omitted_field()
    update: Optional[Dict[str, Dict[str, Any]]] = null_omitted_field()
    destroy: Optional[ListOrRef[str]] = null_omitted_field()


@dataclass
class SetResponse(ResponseWithAccount, SetMethod):
    old_state: Optional[str]
    new_state: Optional[str]
    created: Optional[Dict[str, Any]]
    updated: Optional[Dict[str, Any]]
    destroyed: Optional[List[str]]
    not_created: Optional[Dict[str, SetError]] = null_omitted_field()
    not_updated: Optional[Dict[str, SetError]] = null_omitted_field()
    not_destroyed: Optional[Dict[str, SetError]] = null_omitted_field()


class QueryMethod:
    method_type: Optional[str] = "query"


@dataclass
class Query(MethodWithAccount, QueryMethod):
    sort: Optional[List[Comparator]] = null_omitted_field()
    position: Optional[int] = null_omitted_field()
    anchor: Optional[str] = null_omitted_field()
    anchor_offset: Optional[int] = null_omitted_field()
    limit: Optional[int] = null_omitted_field()
    calculate_total: Optional[bool] = null_omitted_field()


@dataclass
class QueryResponse(ResponseWithAccount, QueryMethod):
    query_state: str
    can_calculate_changes: bool
    position: int
    ids: ListOrRef[str]
    total: Optional[int] = null_omitted_field()
    limit: Optional[int] = null_omitted_field()


class QueryChangesMethod:
    method_type: Optional[str] = "queryChanges"


@dataclass
class QueryChanges(MethodWithAccount, QueryChangesMethod):
    sort: Optional[List[Comparator]] = null_omitted_field()
    since_query_state: Optional[str] = null_omitted_field()
    max_changes: Optional[int] = null_omitted_field()
    up_to_id: Optional[str] = null_omitted_field()
    calculate_total: bool = False


@dataclass
class QueryChangesResponse(ResponseWithAccount, QueryChangesMethod):
    old_query_state: str
    new_query_state: str
    removed: List[str]
    added: List[AddedItem]
    total: Optional[int] = null_omitted_field()


ResponseOrError = Union[Error, Response]
Request = Union[Method, Invocation]
