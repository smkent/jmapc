from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import config

from .. import constants
from ..models import Email, EmailQueryFilter, ListOrRef
from .base import Get, GetResponse, Query, QueryResponse, Set, SetResponse


@dataclass
class EmailGet(Get):
    @classmethod
    def name(cls) -> str:
        return "Email/get"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    body_properties: Optional[List[str]] = None
    fetch_text_body_values: Optional[bool] = None
    fetch_html_body_values: Optional[bool] = field(
        metadata=config(field_name="fetchHTMLBodyValues"), default=None
    )
    fetch_all_body_values: Optional[bool] = None
    max_body_value_bytes: Optional[int] = None


@dataclass
class EmailGetResponse(GetResponse):
    data: List[Email] = field(metadata=config(field_name="list"))


@dataclass
class EmailSet(Set):
    @classmethod
    def name(cls) -> str:
        return "Email/set"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    create: Optional[Dict[str, Email]] = None


@dataclass
class EmailSetResponse(SetResponse):
    created: Optional[Dict[str, Email]]
    updated: Optional[Dict[str, Email]]


@dataclass
class EmailQuery(Query):
    @classmethod
    def name(cls) -> str:
        return "Email/query"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    filter: Optional[EmailQueryFilter] = None
    collapse_threads: Optional[bool] = None


@dataclass
class EmailQueryResponse(QueryResponse):
    ids: ListOrRef[str]
