from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import config

from .. import constants
from ..models import Mailbox, MailboxQueryFilter
from .base import (
    Changes,
    ChangesResponse,
    Get,
    GetResponse,
    Query,
    QueryChanges,
    QueryChangesResponse,
    QueryResponse,
    Set,
    SetResponse,
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
    sort_as_tree: bool = False
    filter_as_tree: bool = False


@dataclass
class MailboxQueryResponse(QueryResponse):
    name = "Mailbox/query"


@dataclass
class MailboxQueryChanges(QueryChanges):
    name = "Mailbox/queryChanges"
    using = set([constants.JMAP_URN_MAIL])

    filter: Optional[MailboxQueryFilter] = None


@dataclass
class MailboxQueryChangesResponse(QueryChangesResponse):
    name = "Mailbox/queryChanges"


@dataclass
class MailboxSet(Set):
    name = "Mailbox/set"
    using = set([constants.JMAP_URN_MAIL])

    create: Optional[Dict[str, Mailbox]] = None
    on_destroy_remove_emails: bool = False


@dataclass
class MailboxSetResponse(SetResponse):
    name = "Mailbox/set"

    created: Optional[Dict[str, Optional[Mailbox]]]
    updated: Optional[Dict[str, Optional[Mailbox]]]
