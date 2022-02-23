from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

from dataclasses_json import config

from ... import constants
from ..util import JsonDataClass
from .methods import JMAPGet, JMAPGetResponse, JMAPQuery, JMAPQueryResponse
from .models import JMAPMailbox, JMAPOperatorLiteral


@dataclass
class JMAPMailboxQuery(JMAPQuery):
    @property
    def name(self) -> str:
        return "Mailbox/query"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    filter: Optional[JMAPMailboxQueryFilter] = None


@dataclass
class JMAPMailboxQueryResponse(JMAPQueryResponse):
    ids: List[str]


@dataclass
class JMAPMailboxQueryFilterCondition(JsonDataClass):
    name: Optional[str] = None
    role: Optional[str] = None
    parent_id: Optional[str] = None


@dataclass
class JMAPMailboxQueryFilterOperator(JsonDataClass):
    operator: JMAPOperatorLiteral
    conditions: List[JMAPMailboxQueryFilter]


JMAPMailboxQueryFilter = Union[
    JMAPMailboxQueryFilterCondition, JMAPMailboxQueryFilterOperator
]


@dataclass
class JMAPMailboxGet(JMAPGet):
    @property
    def name(self) -> str:
        return "Mailbox/get"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_MAIL])


@dataclass
class JMAPMailboxGetResponse(JMAPGetResponse):
    data: List[JMAPMailbox] = field(metadata=config(field_name="list"))
