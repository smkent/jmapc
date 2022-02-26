from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from ..models import Comparator, ListOrRef
from ..serializer import Model


@dataclass
class MethodBase(Model):
    pass


@dataclass
class MethodAccountID(MethodBase):
    account_id: Optional[str] = field(init=False, default=None)


class Method(MethodAccountID):
    @classmethod
    def name(cls) -> str:
        raise NotImplementedError

    @classmethod
    def using(cls) -> set[str]:
        raise NotImplementedError


@dataclass
class Response(MethodBase):
    account_id: Optional[str]


@dataclass
class Get(Method):
    ids: Optional[ListOrRef[str]]
    properties: Optional[List[str]] = None


@dataclass
class GetResponse(Response):
    state: str
    not_found: List[str]


@dataclass
class Query(Method):
    sort: Optional[List[Comparator]] = None


@dataclass
class QueryResponse(Response):
    pass
