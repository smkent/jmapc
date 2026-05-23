from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from dataclasses_json import config

from jmapc import constants
from jmapc.models import Email, EmailQueryFilter

from .base import (
    Changes,
    ChangesResponse,
    Copy,
    CopyResponse,
    Get,
    GetResponse,
    Query,
    QueryChanges,
    QueryChangesResponse,
    QueryResponse,
    Set,
    SetResponse,
)


class EmailBase:
    method_namespace: ClassVar[str | None] = "Email"
    using: ClassVar[set[str]] = {constants.JMAP_URN_MAIL}


@dataclass
class EmailChanges(EmailBase, Changes):
    pass


@dataclass
class EmailChangesResponse(EmailBase, ChangesResponse):
    pass


@dataclass
class EmailCopy(EmailBase, Copy):
    create: dict[str, Email] | None = None


@dataclass
class EmailCopyResponse(EmailBase, CopyResponse):
    created: dict[str, Email] | None = None


@dataclass
class EmailGet(EmailBase, Get):
    body_properties: list[str] | None = None
    fetch_text_body_values: bool | None = None
    fetch_html_body_values: bool | None = field(
        metadata=config(field_name="fetchHTMLBodyValues"), default=None
    )
    fetch_all_body_values: bool | None = None
    max_body_value_bytes: int | None = None


@dataclass
class EmailGetResponse(EmailBase, GetResponse):
    data: list[Email] = field(metadata=config(field_name="list"))


@dataclass
class EmailQuery(EmailBase, Query):
    filter: EmailQueryFilter | None = None
    collapse_threads: bool | None = None


@dataclass
class EmailQueryResponse(EmailBase, QueryResponse):
    pass


@dataclass
class EmailQueryChanges(EmailBase, QueryChanges):
    filter: EmailQueryFilter | None = None
    collapse_threads: bool | None = None


@dataclass
class EmailQueryChangesResponse(EmailBase, QueryChangesResponse):
    pass


@dataclass
class EmailSet(EmailBase, Set):
    create: dict[str, Email] | None = None


@dataclass
class EmailSetResponse(EmailBase, SetResponse):
    created: dict[str, Email | None] | None
    updated: dict[str, Email | None] | None
