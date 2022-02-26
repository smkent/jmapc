from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Union

from dataclasses_json import config

from .. import constants
from ..models import Email, JMAPList, JMAPStr, Operator
from ..util import JsonDataClass, datetime_decode, datetime_encode
from .methods import Get, GetResponse, Query, QueryResponse


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
    ids: JMAPList[str]


@dataclass
class EmailQueryFilterCondition(JsonDataClass):
    in_mailbox: Optional[JMAPStr] = None
    in_mailbox_other_than: Optional[JMAPList] = None
    before: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    after: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    min_size: Optional[int] = None
    max_size: Optional[int] = None
    all_in_thread_have_keyword: Optional[JMAPStr] = None
    some_in_thread_have_keyword: Optional[JMAPStr] = None
    none_in_thread_have_keyword: Optional[JMAPStr] = None
    has_keyword: Optional[JMAPStr] = None
    not_keyword: Optional[JMAPStr] = None
    has_attachment: Optional[bool] = None
    text: Optional[JMAPStr] = None
    mail_from: Optional[str] = field(
        metadata=config(field_name="from"), default=None
    )
    to: Optional[JMAPStr] = None
    cc: Optional[JMAPStr] = None
    bcc: Optional[JMAPStr] = None
    body: Optional[JMAPStr] = None
    header: Optional[JMAPList] = None


@dataclass
class EmailQueryFilterOperator(JsonDataClass):
    operator: Operator
    conditions: List[EmailQueryFilter]


EmailQueryFilter = Union[EmailQueryFilterCondition, EmailQueryFilterOperator]


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
    fetch_html_body_values: Optional[bool] = None
    fetch_all_body_values: Optional[bool] = None
    max_body_value_bytes: Optional[int] = None


@dataclass
class EmailGetResponse(GetResponse):
    data: List[Email] = field(metadata=config(field_name="list"))
