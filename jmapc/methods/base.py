from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..models import Comparator, ListOrRef, SetError, StrOrRef
from ..serializer import Model


@dataclass
class MethodBase(Model):
    pass


class Method(MethodBase):
    name = ""
    using: set[str] = set()


@dataclass
class MethodWithAccount(Method):
    account_id: Optional[str] = field(init=False, default=None)


@dataclass
class Response(MethodBase):
    pass


@dataclass
class ResponseWithAccount(Response):
    account_id: Optional[str]


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
    pass
