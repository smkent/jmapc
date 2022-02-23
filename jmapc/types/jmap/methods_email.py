from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import config

from ... import constants
from ..util import JsonDataClass
from .methods import JMAPMethod, JMAPResponse
from .models import JMAPEmail


@dataclass
class JMAPEmailQuery(JMAPMethod):
    @property
    def name(self) -> str:
        return "Email/query"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    filter: Optional[JMAPEmailQueryFilter]
    collapse_threads: Optional[bool]


@dataclass
class JMAPEmailQueryResponse(JMAPResponse):
    ids: List[str]


@dataclass
class JMAPEmailQueryFilter(JsonDataClass):
    in_mailbox: str


@dataclass
class JMAPEmailGet(JMAPMethod):
    @property
    def name(self) -> str:
        return "Email/get"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    ids: List[str]
    properties: Optional[List[str]] = None
    body_properties: Optional[List[str]] = None
    fetch_text_body_values: Optional[bool] = None
    fetch_html_body_values: Optional[bool] = None
    fetch_all_body_values: Optional[bool] = None
    max_body_value_bytes: Optional[int] = None


@dataclass
class JMAPEmailGetResponse(JMAPResponse):
    data: List[JMAPEmail] = field(metadata=config(field_name="list"))
