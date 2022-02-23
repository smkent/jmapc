from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from ..util import JsonDataClass
from .models import JMAPComparator, JMAPList


@dataclass
class JMAPMethodBase(JsonDataClass):
    pass


@dataclass
class JMAPMethodAccountID(JMAPMethodBase):
    account_id: Optional[str] = field(init=False, default=None)


class JMAPMethod(JMAPMethodAccountID):
    @classmethod
    def name(cls) -> str:
        raise NotImplementedError

    @classmethod
    def using(cls) -> set[str]:
        raise NotImplementedError


@dataclass
class JMAPResponse(JMAPMethodBase):
    account_id: Optional[str]


@dataclass
class JMAPGet(JMAPMethod):
    ids: Optional[JMAPList[str]]
    properties: Optional[List[str]] = None


@dataclass
class JMAPGetResponse(JMAPResponse):
    state: str
    not_found: List[str]


@dataclass
class JMAPQuery(JMAPMethod):
    sort: Optional[List[JMAPComparator]] = None


@dataclass
class JMAPQueryResponse(JMAPResponse):
    pass
