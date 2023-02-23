from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import config

from .. import constants
from ..models import Email, EmailQueryFilter
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
    method_namespace: Optional[str] = "Email"
    using = {constants.JMAP_URN_MAIL}


@dataclass
class EmailChanges(EmailBase, Changes):
    pass


@dataclass
class EmailChangesResponse(EmailBase, ChangesResponse):
    pass


@dataclass
class EmailCopy(EmailBase, Copy):
    create: Optional[Dict[str, Email]] = None


@dataclass
class EmailCopyResponse(EmailBase, CopyResponse):
    created: Optional[Dict[str, Email]] = None


@dataclass
class EmailGet(EmailBase, Get):
    body_properties: Optional[List[str]] = None
    fetch_text_body_values: Optional[bool] = None
    fetch_html_body_values: Optional[bool] = field(
        metadata=config(field_name="fetchHTMLBodyValues"), default=None
    )
    fetch_all_body_values: Optional[bool] = None
    max_body_value_bytes: Optional[int] = None


@dataclass
class EmailGetResponse(EmailBase, GetResponse):
    data: List[Email] = field(metadata=config(field_name="list"))


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
    create: Optional[Dict[str, Email]] = None


@dataclass
class EmailSetResponse(EmailBase, SetResponse):
    created: Optional[Dict[str, Optional[Email]]]
    updated: Optional[Dict[str, Optional[Email]]]
