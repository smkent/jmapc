from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

from dataclasses_json import config

from .. import constants
from ..models import JMAPList, JMAPStr, Mailbox, Operator
from ..util import JsonDataClass
from .methods import Get, GetResponse, Query, QueryResponse


@dataclass
class MailboxQuery(Query):
    @classmethod
    def name(cls) -> str:
        return "Mailbox/query"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    filter: Optional[MailboxQueryFilter] = None


@dataclass
class MailboxQueryResponse(QueryResponse):
    ids: JMAPList[str]


@dataclass
class MailboxQueryFilterCondition(JsonDataClass):
    name: Optional[JMAPStr] = None
    role: Optional[JMAPStr] = None
    parent_id: Optional[JMAPStr] = None


@dataclass
class MailboxQueryFilterOperator(JsonDataClass):
    operator: Operator
    conditions: List[MailboxQueryFilter]


MailboxQueryFilter = Union[
    MailboxQueryFilterCondition, MailboxQueryFilterOperator
]


@dataclass
class MailboxGet(Get):
    @classmethod
    def name(cls) -> str:
        return "Mailbox/get"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])


@dataclass
class MailboxGetResponse(GetResponse):
    data: List[Mailbox] = field(metadata=config(field_name="list"))
