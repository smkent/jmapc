from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from ..models import Comparator, ListOrRef
from ..serializer import Model


@dataclass
class MethodBase(Model):
    pass


class Method(MethodBase):
    @classmethod
    def name(cls) -> str:
        raise NotImplementedError

    @classmethod
    def using(cls) -> set[str]:
        raise NotImplementedError


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
    state: str
    not_found: List[str]


@dataclass
class Query(MethodWithAccount):
    sort: Optional[List[Comparator]] = None


@dataclass
class QueryResponse(ResponseWithAccount):
    pass
