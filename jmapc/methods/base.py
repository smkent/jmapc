from __future__ import annotations

import contextlib
from dataclasses import dataclass, field
from typing import Any, ClassVar, cast

from jmapc.errors import Error
from jmapc.models import AddedItem, Comparator, ListOrRef, SetError, StrOrRef
from jmapc.serializer import Model


class MethodBase(Model):
    method_namespace: ClassVar[str | None] = None
    using: ClassVar[set[str]] = set()

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
    account_id: str | None = field(init=False, default=None)


class ResponseCollector(MethodBase):
    response_types: ClassVar[dict[str, type[Error | Response]]] = {}

    @classmethod
    def __init_subclass__(cls) -> None:
        with contextlib.suppress(ValueError):
            method_name = cls.get_method_name()
            ResponseCollector.response_types[method_name] = cast(
                "type[Response]", cls
            )


@dataclass
class Response(ResponseCollector):
    pass


@dataclass
class ResponseWithAccount(Response):
    account_id: str | None


@dataclass
class InvocationBase:
    id: str


@dataclass
class Invocation(InvocationBase):
    method: Method


@dataclass
class InvocationResponse(InvocationBase):
    response: Response


@dataclass
class InvocationResponseOrError(InvocationBase):
    response: Error | Response


class ChangesMethod:
    method_type: str | None = "changes"


@dataclass
class Changes(MethodWithAccount, ChangesMethod):
    since_state: str
    max_changes: int | None = None


@dataclass
class ChangesResponse(ResponseWithAccount, ChangesMethod):
    old_state: str
    new_state: str
    has_more_changes: bool
    created: list[str]
    updated: list[str]
    destroyed: list[str]


class CopyMethod:
    method_type: str | None = "copy"


@dataclass
class Copy(MethodWithAccount, CopyMethod):
    from_account_id: str
    if_from_in_state: str | None = None
    if_in_state: str | None = None
    on_success_destroy_original: bool = False
    destroy_from_if_in_state: str | None = None


@dataclass
class CopyResponse(ResponseWithAccount, CopyMethod):
    from_account_id: str
    old_state: str
    new_state: str
    not_created: dict[str, SetError] | None


class GetMethod:
    method_type: str | None = "get"


@dataclass
class Get(MethodWithAccount, GetMethod):
    ids: ListOrRef[str] | None
    properties: list[str] | None = None


@dataclass
class GetResponseWithoutState(ResponseWithAccount, GetMethod):
    not_found: list[str] | None


@dataclass
class GetResponse(GetResponseWithoutState):
    state: str | None


class SetMethod:
    method_type: str | None = "set"


@dataclass
class Set(MethodWithAccount, SetMethod):
    if_in_state: StrOrRef | None = None
    create: dict[str, Any] | None = None
    update: dict[str, dict[str, Any]] | None = None
    destroy: ListOrRef[str] | None = None


@dataclass
class SetResponse(ResponseWithAccount, SetMethod):
    old_state: str | None
    new_state: str | None
    created: dict[str, Any] | None
    updated: dict[str, Any] | None
    destroyed: list[str] | None
    not_created: dict[str, SetError] | None = None
    not_updated: dict[str, SetError] | None = None
    not_destroyed: dict[str, SetError] | None = None


class QueryMethod:
    method_type: str | None = "query"


@dataclass
class Query(MethodWithAccount, QueryMethod):
    sort: list[Comparator] | None = None
    position: int | None = None
    anchor: str | None = None
    anchor_offset: int | None = None
    limit: int | None = None
    calculate_total: bool | None = None


@dataclass
class QueryResponse(ResponseWithAccount, QueryMethod):
    query_state: str
    can_calculate_changes: bool
    position: int
    ids: ListOrRef[str]
    total: int | None = None
    limit: int | None = None


class QueryChangesMethod:
    method_type: str | None = "queryChanges"


@dataclass
class QueryChanges(MethodWithAccount, QueryChangesMethod):
    sort: list[Comparator] | None = None
    since_query_state: str | None = None
    max_changes: int | None = None
    up_to_id: str | None = None
    calculate_total: bool = False


@dataclass
class QueryChangesResponse(ResponseWithAccount, QueryChangesMethod):
    old_query_state: str
    new_query_state: str
    removed: list[str]
    added: list[AddedItem]
    total: int | None = None


ResponseOrError = Error | Response
Request = Method | Invocation
