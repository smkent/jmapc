from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Literal, Optional, TypeVar, Union

from dataclasses_json import config

from .util import (
    JsonDataClass,
    ResultReference,
    datetime_decode,
    datetime_encode,
)

T = TypeVar("T")


JMAPStr = Union[str, ResultReference]
JMAPList = Union[ResultReference, List[T]]


@dataclass
class Identity(JsonDataClass):
    id: str
    name: str
    email: str
    replyTo: Optional[str]
    bcc: Optional[List[IdentityBCC]]
    textSignature: Optional[str]
    htmlSignature: Optional[str]
    mayDelete: bool


@dataclass
class IdentityBCC(JsonDataClass):
    name: Optional[str]
    email: str


@dataclass
class Mailbox(JsonDataClass):
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
class Email(JsonDataClass):
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
    headers: Optional[List[EmailHeader]] = None
    mail_from: Optional[List[EmailAddress]] = field(
        metadata=config(field_name="from"), default=None
    )
    to: Optional[List[EmailAddress]] = None
    cc: Optional[List[EmailAddress]] = None
    bcc: Optional[List[EmailAddress]] = None
    subject: Optional[str] = None
    sent_at: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    body_structure: Optional[EmailBodyPart] = None
    body_values: Optional[Dict[str, EmailBodyValue]] = None
    text_body: Optional[List[EmailBodyPart]] = None
    html_body: Optional[List[EmailBodyPart]] = None
    attachments: Optional[List[EmailBodyPart]] = None
    has_attachment: Optional[bool] = None
    preview: Optional[str] = None


@dataclass
class EmailAddress(JsonDataClass):
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class EmailHeader(JsonDataClass):
    name: Optional[str] = None
    value: Optional[str] = None


@dataclass
class EmailBodyPart(JsonDataClass):
    part_id: Optional[str] = None
    blob_id: Optional[str] = None
    size: Optional[int] = None
    headers: Optional[List[EmailHeader]] = None
    name: Optional[str] = None
    type: Optional[str] = None
    charset: Optional[str] = None
    disposition: Optional[str] = None
    cid: Optional[str] = None
    language: Optional[List[str]] = None
    location: Optional[str] = None
    sub_parts: Optional[List[EmailBodyPart]] = None


@dataclass
class EmailBodyValue(JsonDataClass):
    value: Optional[str] = None
    is_encoding_problem: Optional[bool] = None
    is_truncated: Optional[bool] = None


@dataclass
class Thread(JsonDataClass):
    def __len__(self) -> int:
        return len(self.email_ids)

    id: str
    email_ids: List[str]


@dataclass
class ThreadEmail(JsonDataClass):
    id: str
    mailbox_ids: List[str]
    is_unread: bool
    is_flagged: bool


@dataclass
class Comparator(JsonDataClass):
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


OperatorLiteral = Union[Literal["AND"], Literal["OR"], Literal["NOT"]]