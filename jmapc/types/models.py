from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Literal, Optional, TypeVar, Union

from dataclasses_json import config

from .util import (
    JMAPResultReference,
    JsonDataClass,
    datetime_decode,
    datetime_encode,
)

T = TypeVar("T")


JMAPStr = Union[str, JMAPResultReference]
JMAPList = Union[JMAPResultReference, List[T]]


@dataclass
class JMAPIdentity(JsonDataClass):
    id: str
    name: str
    email: str
    replyTo: Optional[str]
    bcc: Optional[List[JMAPIdentityBCC]]
    textSignature: Optional[str]
    htmlSignature: Optional[str]
    mayDelete: bool


@dataclass
class JMAPIdentityBCC(JsonDataClass):
    name: Optional[str]
    email: str


@dataclass
class JMAPMailbox(JsonDataClass):
    id: str = field(metadata=config(field_name="Id"))
    name: str
    sort_order: int = field(metadata=config(field_name="sortOrder"))
    total_emails: int = field(metadata=config(field_name="totalEmails"))
    unread_emails: int = field(metadata=config(field_name="unreadEmails"))
    total_threads: int = field(metadata=config(field_name="totalThreads"))
    unread_threads: int = field(metadata=config(field_name="unreadThreads"))
    is_subsribed: bool = field(metadata=config(field_name="isSubscribed"))
    role: Optional[str] = None
    parent_id: Optional[str] = field(
        metadata=config(field_name="parentId"), default=None
    )


@dataclass
class JMAPEmail(JsonDataClass):
    id: str = field(metadata=config(field_name="Id"))
    blob_id: Optional[str] = None
    thread_id: Optional[str] = None
    mailbox_ids: Optional[Dict[str, bool]] = None
    keywords: Optional[Dict[str, bool]] = None
    size: Optional[int] = None
    received_at: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    message_id: Optional[List[str]] = None
    in_reply_to: Optional[List[str]] = None
    references: Optional[List[str]] = None
    headers: Optional[List[JMAPEmailHeader]] = None
    mail_from: Optional[List[JMAPEmailAddress]] = field(
        metadata=config(field_name="from"), default=None
    )
    to: Optional[List[JMAPEmailAddress]] = None
    cc: Optional[List[JMAPEmailAddress]] = None
    bcc: Optional[List[JMAPEmailAddress]] = None
    subject: Optional[str] = None
    sent_at: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    body_structure: Optional[JMAPEmailBodyPart] = None
    body_values: Optional[Dict[str, JMAPEmailBodyValue]] = None
    text_body: Optional[List[JMAPEmailBodyPart]] = None
    html_body: Optional[List[JMAPEmailBodyPart]] = None
    attachments: Optional[List[JMAPEmailBodyPart]] = None
    has_attachment: Optional[bool] = None
    preview: Optional[str] = None


@dataclass
class JMAPEmailAddress(JsonDataClass):
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class JMAPEmailHeader(JsonDataClass):
    name: Optional[str] = None
    value: Optional[str] = None


@dataclass
class JMAPEmailBodyPart(JsonDataClass):
    part_id: Optional[str] = None
    blob_id: Optional[str] = None
    size: Optional[int] = None
    headers: Optional[List[JMAPEmailHeader]] = None
    name: Optional[str] = None
    type: Optional[str] = None
    charset: Optional[str] = None
    disposition: Optional[str] = None
    cid: Optional[str] = None
    language: Optional[List[str]] = None
    location: Optional[str] = None
    sub_parts: Optional[List[JMAPEmailBodyPart]] = None


@dataclass
class JMAPEmailBodyValue(JsonDataClass):
    value: Optional[str] = None
    is_encoding_problem: Optional[bool] = None
    is_truncated: Optional[bool] = None


@dataclass
class JMAPThread(JsonDataClass):
    def __len__(self) -> int:
        return len(self.email_ids)

    id: str
    email_ids: List[str]


@dataclass
class JMAPThreadEmail(JsonDataClass):
    id: str
    mailbox_ids: List[str]
    is_unread: bool
    is_flagged: bool


@dataclass
class JMAPComparator(JsonDataClass):
    property: str
    is_ascending: bool = True
    collation: Optional[str] = None
    anchor: Optional[str] = None
    anchor_offset: int = 0
    limit: Optional[int] = None
    calculate_total: bool = False
    position: int = 0


@dataclass
class JMAPFilterOperator(JsonDataClass):
    operator: Union[Literal["AND"], Literal["OR"], Literal["NOT"]]


JMAPOperatorLiteral = Union[Literal["AND"], Literal["OR"], Literal["NOT"]]
