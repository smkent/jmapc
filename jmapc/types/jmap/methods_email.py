from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

from dataclasses_json import config

from ... import constants
from ..util import JsonDataClass
from .methods import JMAPGet, JMAPGetResponse, JMAPQuery, JMAPQueryResponse
from .models import JMAPEmail, JMAPList, JMAPOperatorLiteral, JMAPStr


@dataclass
class JMAPEmailQuery(JMAPQuery):
    @classmethod
    def name(cls) -> str:
        return "Email/query"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    filter: Optional[JMAPEmailQueryFilter] = None
    collapse_threads: Optional[bool] = None


@dataclass
class JMAPEmailQueryResponse(JMAPQueryResponse):
    ids: JMAPList[str]


@dataclass
class JMAPEmailQueryFilterCondition(JsonDataClass):
    in_mailbox: Optional[JMAPStr]


@dataclass
class JMAPEmailQueryFilterOperator(JsonDataClass):
    operator: JMAPOperatorLiteral
    conditions: List[JMAPEmailQueryFilter]


JMAPEmailQueryFilter = Union[
    JMAPEmailQueryFilterCondition, JMAPEmailQueryFilterOperator
]


@dataclass
class JMAPEmailGet(JMAPGet):
    @classmethod
    def name(cls) -> str:
        return "Email/get"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    body_properties: Optional[List[str]] = None
    fetch_text_body_values: Optional[bool] = None
    fetch_html_body_values: Optional[bool] = None
    fetch_all_body_values: Optional[bool] = None
    max_body_value_bytes: Optional[int] = None


@dataclass
class JMAPEmailGetResponse(JMAPGetResponse):
    data: List[JMAPEmail] = field(metadata=config(field_name="list"))
