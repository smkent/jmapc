from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from dataclasses_json import config

from jmapc import constants
from jmapc.models import Mailbox, MailboxQueryFilter

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


class MailboxBase:
    method_namespace: ClassVar[str | None] = "Mailbox"
    using: ClassVar[set[str]] = {constants.JMAP_URN_MAIL}


@dataclass
class MailboxChanges(MailboxBase, Changes):
    pass


@dataclass
class MailboxChangesResponse(MailboxBase, ChangesResponse):
    pass


@dataclass
class MailboxGet(MailboxBase, Get):
    pass


@dataclass
class MailboxGetResponse(MailboxBase, GetResponse):
    data: list[Mailbox] = field(metadata=config(field_name="list"))


@dataclass
class MailboxQuery(MailboxBase, Query):
    filter: MailboxQueryFilter | None = None
    sort_as_tree: bool = False
    filter_as_tree: bool = False


@dataclass
class MailboxQueryResponse(MailboxBase, QueryResponse):
    pass


@dataclass
class MailboxQueryChanges(MailboxBase, QueryChanges):
    filter: MailboxQueryFilter | None = None


@dataclass
class MailboxQueryChangesResponse(MailboxBase, QueryChangesResponse):
    pass


@dataclass
class MailboxSet(MailboxBase, Set):
    create: dict[str, Mailbox] | None = None
    on_destroy_remove_emails: bool = False


@dataclass
class MailboxSetResponse(MailboxBase, SetResponse):
    created: dict[str, Mailbox | None] | None
    updated: dict[str, Mailbox | None] | None
