from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import config

from .. import constants
from ..models import ListOrRef, Mailbox, MailboxQueryFilter
from .base import Get, GetResponse, Query, QueryResponse, Set, SetResponse


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


@dataclass
class MailboxSet(Set):
    name = "Mailbox/set"
    using = set([constants.JMAP_URN_MAIL])

    create: Optional[Dict[str, Mailbox]] = None
    on_destroy_remove_emails: bool = False


@dataclass
class MailboxSetResponse(SetResponse):
    name = "Mailbox/set"
    using = set([constants.JMAP_URN_MAIL])

    created: Optional[Dict[str, Optional[Mailbox]]]
    updated: Optional[Dict[str, Optional[Mailbox]]]
