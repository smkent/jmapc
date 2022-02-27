from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import config

from .. import constants
from ..models import ListOrRef, Mailbox, MailboxQueryFilter
from .base import Get, GetResponse, Query, QueryResponse


@dataclass
class MailboxGet(Get):
    def __post_init__(self) -> None:
        self.name = "Mailbox/get"
        self.using = set([constants.JMAP_URN_MAIL])


@dataclass
class MailboxGetResponse(GetResponse):
    data: List[Mailbox] = field(metadata=config(field_name="list"))


@dataclass
class MailboxQuery(Query):
    def __post_init__(self) -> None:
        self.name = "Mailbox/query"
        self.using = set([constants.JMAP_URN_MAIL])

    filter: Optional[MailboxQueryFilter] = None


@dataclass
class MailboxQueryResponse(QueryResponse):
    ids: ListOrRef[str]
