from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

from dataclasses_json import config

from .. import constants
from .methods import JMAPGet, JMAPGetResponse, JMAPQuery, JMAPQueryResponse
from .models import JMAPList, JMAPMailbox, JMAPOperatorLiteral, JMAPStr
from .util import JsonDataClass


@dataclass
class JMAPMailboxQuery(JMAPQuery):
    @classmethod
    def name(cls) -> str:
        return "Mailbox/query"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    filter: Optional[JMAPMailboxQueryFilter] = None


@dataclass
class JMAPMailboxQueryResponse(JMAPQueryResponse):
    ids: JMAPList[str]


@dataclass
class JMAPMailboxQueryFilterCondition(JsonDataClass):
    name: Optional[JMAPStr] = None
    role: Optional[JMAPStr] = None
    parent_id: Optional[JMAPStr] = None


@dataclass
class JMAPMailboxQueryFilterOperator(JsonDataClass):
    operator: JMAPOperatorLiteral
    conditions: List[JMAPMailboxQueryFilter]


JMAPMailboxQueryFilter = Union[
    JMAPMailboxQueryFilterCondition, JMAPMailboxQueryFilterOperator
]


@dataclass
class JMAPMailboxGet(JMAPGet):
    @classmethod
    def name(cls) -> str:
        return "Mailbox/get"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])


@dataclass
class JMAPMailboxGetResponse(JMAPGetResponse):
    data: List[JMAPMailbox] = field(metadata=config(field_name="list"))
