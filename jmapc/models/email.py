from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union

from dataclasses_json import config

from ..serializer import Model, datetime_decode, datetime_encode
from .models import EmailAddress, ListOrRef, Operator, StrOrRef


@dataclass
class Email(Model):
    id: Optional[str] = field(metadata=config(field_name="id"), default=None)
    blob_id: Optional[str] = None
    thread_id: Optional[str] = None
    mailbox_ids: Optional[dict[str, bool]] = None
    keywords: Optional[dict[str, bool]] = None
    size: Optional[int] = None
    received_at: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    message_id: Optional[list[str]] = None
    in_reply_to: Optional[list[str]] = None
    references: Optional[list[str]] = None
    headers: Optional[list[EmailHeader]] = None
    mail_from: Optional[list[EmailAddress]] = field(
        metadata=config(field_name="from"), default=None
    )
    to: Optional[list[EmailAddress]] = None
    cc: Optional[list[EmailAddress]] = None
    bcc: Optional[list[EmailAddress]] = None
    reply_to: Optional[list[EmailAddress]] = None
    subject: Optional[str] = None
    sent_at: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    body_structure: Optional[EmailBodyPart] = None
    body_values: Optional[dict[str, EmailBodyValue]] = None
    text_body: Optional[list[EmailBodyPart]] = None
    html_body: Optional[list[EmailBodyPart]] = None
    attachments: Optional[list[EmailBodyPart]] = None
    has_attachment: Optional[bool] = None
    preview: Optional[str] = None


@dataclass
class EmailHeader(Model):
    name: Optional[str] = None
    value: Optional[str] = None


@dataclass
class EmailBodyPart(Model):
    part_id: Optional[str] = None
    blob_id: Optional[str] = None
    size: Optional[int] = None
    headers: Optional[list[EmailHeader]] = None
    name: Optional[str] = None
    type: Optional[str] = None
    charset: Optional[str] = None
    disposition: Optional[str] = None
    cid: Optional[str] = None
    language: Optional[list[str]] = None
    location: Optional[str] = None
    sub_parts: Optional[list[EmailBodyPart]] = None


@dataclass
class EmailBodyValue(Model):
    value: Optional[str] = None
    is_encoding_problem: Optional[bool] = None
    is_truncated: Optional[bool] = None


@dataclass
class EmailQueryFilterCondition(Model):
    in_mailbox: Optional[StrOrRef] = None
    in_mailbox_other_than: Optional[ListOrRef[str]] = None
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
    all_in_thread_have_keyword: Optional[StrOrRef] = None
    some_in_thread_have_keyword: Optional[StrOrRef] = None
    none_in_thread_have_keyword: Optional[StrOrRef] = None
    has_keyword: Optional[StrOrRef] = None
    not_keyword: Optional[StrOrRef] = None
    has_attachment: Optional[bool] = None
    text: Optional[StrOrRef] = None
    mail_from: Optional[str] = field(
        metadata=config(field_name="from"), default=None
    )
    to: Optional[StrOrRef] = None
    cc: Optional[StrOrRef] = None
    bcc: Optional[StrOrRef] = None
    body: Optional[StrOrRef] = None
    header: Optional[ListOrRef[str]] = None


@dataclass
class EmailQueryFilterOperator(Model):
    operator: Operator
    conditions: list[EmailQueryFilter]


EmailQueryFilter = Union[EmailQueryFilterCondition, EmailQueryFilterOperator]
