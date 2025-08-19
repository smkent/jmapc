from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import config

from .. import constants
from ..models import Email, EmailImport, EmailQueryFilter, SetError
from .base import (
    Changes,
    ChangesResponse,
    Copy,
    CopyResponse,
    Get,
    GetResponse,
    MethodWithAccount,
    Query,
    QueryChanges,
    QueryChangesResponse,
    QueryResponse,
    ResponseWithAccount,
    Set,
    SetResponse,
)


class EmailBase:
    method_namespace: Optional[str] = "Email"
    using = {constants.JMAP_URN_MAIL}


@dataclass
class EmailChanges(EmailBase, Changes):
    pass


@dataclass
class EmailChangesResponse(EmailBase, ChangesResponse):
    pass


class EmailImportMethod:
    method_type: Optional[str] = "import"


@dataclass
class EmailImportRequest(EmailBase, EmailImportMethod, MethodWithAccount):
    """
    Email/import request.

    See https://datatracker.ietf.org/doc/html/rfc8621#section-4.8
    """

    emails: dict[str, EmailImport] = field(default_factory=dict)
    if_in_state: Optional[str] = field(
        metadata=config(field_name="ifInState"), default=None
    )


@dataclass
class EmailImportResponse(EmailBase, EmailImportMethod, ResponseWithAccount):
    """
    Email/import response.

    See https://datatracker.ietf.org/doc/html/rfc8621#section-4.8
    """

    old_state: Optional[str] = field(metadata=config(field_name="oldState"))
    new_state: str = field(metadata=config(field_name="newState"))
    created: Optional[dict[str, Email]] = None
    not_created: Optional[dict[str, SetError]] = field(
        metadata=config(field_name="notCreated"), default=None
    )


@dataclass
class EmailCopy(EmailBase, Copy):
    create: Optional[dict[str, Email]] = None


@dataclass
class EmailCopyResponse(EmailBase, CopyResponse):
    created: Optional[dict[str, Email]] = None


@dataclass
class EmailGet(EmailBase, Get):
    body_properties: Optional[list[str]] = None
    fetch_text_body_values: Optional[bool] = None
    fetch_html_body_values: Optional[bool] = field(
        metadata=config(field_name="fetchHTMLBodyValues"), default=None
    )
    fetch_all_body_values: Optional[bool] = None
    max_body_value_bytes: Optional[int] = None


@dataclass
class EmailGetResponse(EmailBase, GetResponse):
    data: list[Email] = field(metadata=config(field_name="list"))


@dataclass
class EmailQuery(EmailBase, Query):
    filter: Optional[EmailQueryFilter] = None
    collapse_threads: Optional[bool] = None


@dataclass
class EmailQueryResponse(EmailBase, QueryResponse):
    pass


@dataclass
class EmailQueryChanges(EmailBase, QueryChanges):
    filter: Optional[EmailQueryFilter] = None
    collapse_threads: Optional[bool] = None


@dataclass
class EmailQueryChangesResponse(EmailBase, QueryChangesResponse):
    pass


@dataclass
class EmailSet(EmailBase, Set):
    create: Optional[dict[str, Email]] = None


@dataclass
class EmailSetResponse(EmailBase, SetResponse):
    created: Optional[dict[str, Optional[Email]]]
    updated: Optional[dict[str, Optional[Email]]]
