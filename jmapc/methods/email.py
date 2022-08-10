from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import config

from .. import constants
from ..models import Email, EmailQueryFilter
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
class EmailChanges(Changes):
    name = "Email/changes"
    using = set([constants.JMAP_URN_MAIL])


@dataclass
class EmailChangesResponse(ChangesResponse):
    name = "Email/changes"


@dataclass
class EmailGet(Get):
    name = "Email/get"
    using = set([constants.JMAP_URN_MAIL])

    body_properties: Optional[List[str]] = None
    fetch_text_body_values: Optional[bool] = None
    fetch_html_body_values: Optional[bool] = field(
        metadata=config(field_name="fetchHTMLBodyValues"), default=None
    )
    fetch_all_body_values: Optional[bool] = None
    max_body_value_bytes: Optional[int] = None


@dataclass
class EmailGetResponse(GetResponse):
    name = "Email/get"

    data: List[Email] = field(metadata=config(field_name="list"))


@dataclass
class EmailSet(Set):
    name = "Email/set"
    using = set([constants.JMAP_URN_MAIL])

    create: Optional[Dict[str, Email]] = None


@dataclass
class EmailSetResponse(SetResponse):
    name = "Email/set"

    created: Optional[Dict[str, Optional[Email]]]
    updated: Optional[Dict[str, Optional[Email]]]


@dataclass
class EmailQuery(Query):
    name = "Email/query"
    using = set([constants.JMAP_URN_MAIL])

    filter: Optional[EmailQueryFilter] = None
    collapse_threads: Optional[bool] = None


@dataclass
class EmailQueryResponse(QueryResponse):
    name = "Email/query"


@dataclass
class EmailQueryChanges(QueryChanges):
    name = "Email/queryChanges"
    using = set([constants.JMAP_URN_MAIL])

    filter: Optional[EmailQueryFilter] = None
    collapse_threads: Optional[bool] = None


@dataclass
class EmailQueryChangesResponse(QueryChangesResponse):
    name = "Email/queryChanges"
