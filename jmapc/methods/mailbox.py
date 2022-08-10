from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import config

from .. import constants
from ..models import ListOrRef, Mailbox, MailboxQueryFilter
from .base import (
    Changes,
    ChangesResponse,
    Get,
    GetResponse,
    Query,
    QueryResponse,
)


@dataclass
class MailboxChanges(Changes):
    name = "Mailbox/changes"
    using = set([constants.JMAP_URN_MAIL])


@dataclass
class MailboxChangesResponse(ChangesResponse):
    name = "Mailbox/changes"


@dataclass
class MailboxGet(Get):
    name = "Mailbox/get"
    using = set([constants.JMAP_URN_MAIL])


@dataclass
class MailboxGetResponse(GetResponse):
    name = "Mailbox/get"

    data: List[Mailbox] = field(metadata=config(field_name="list"))


@dataclass
class MailboxQuery(Query):
    name = "Mailbox/query"
    using = set([constants.JMAP_URN_MAIL])

    filter: Optional[MailboxQueryFilter] = None


@dataclass
class MailboxQueryResponse(QueryResponse):
    name = "Mailbox/query"

    ids: ListOrRef[str]
