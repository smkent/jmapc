from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Union

from dataclasses_json import config

from ..serializer import (
    Model,
    datetime_decode,
    datetime_encode,
    null_omitted_field,
)
from .models import EmailAddress, ListOrRef, Operator, StrOrRef


@dataclass
class Email(Model):
    id: Optional[str] = field(metadata=config(field_name="id"), default=None)
    blob_id: Optional[str] = null_omitted_field()
    thread_id: Optional[str] = null_omitted_field()
    mailbox_ids: Optional[Dict[str, bool]] = null_omitted_field()
    keywords: Optional[Dict[str, bool]] = null_omitted_field()
    size: Optional[int] = null_omitted_field()
    received_at: Optional[datetime] = null_omitted_field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    message_id: Optional[List[str]] = null_omitted_field()
    in_reply_to: Optional[List[str]] = null_omitted_field()
    references: Optional[List[str]] = null_omitted_field()
    headers: Optional[List[EmailHeader]] = null_omitted_field()
    mail_from: Optional[List[EmailAddress]] = null_omitted_field(
        default=None, metadata=config(field_name="from")
    )
    to: Optional[List[EmailAddress]] = null_omitted_field()
    cc: Optional[List[EmailAddress]] = null_omitted_field()
    bcc: Optional[List[EmailAddress]] = null_omitted_field()
    reply_to: Optional[List[EmailAddress]] = null_omitted_field()
    subject: Optional[str] = null_omitted_field()
    sent_at: Optional[datetime] = null_omitted_field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    body_structure: Optional[EmailBodyPart] = null_omitted_field()
    body_values: Optional[Dict[str, EmailBodyValue]] = null_omitted_field()
    text_body: Optional[List[EmailBodyPart]] = null_omitted_field()
    html_body: Optional[List[EmailBodyPart]] = null_omitted_field()
    attachments: Optional[List[EmailBodyPart]] = null_omitted_field()
    has_attachment: Optional[bool] = null_omitted_field()
    preview: Optional[str] = null_omitted_field()


@dataclass
class EmailHeader(Model):
    name: Optional[str] = None
    value: Optional[str] = None


@dataclass
class EmailBodyPart(Model):
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
    mail_from: Optional[str] = null_omitted_field(
        default=None,
        metadata=config(field_name="from"),
    )
    to: Optional[StrOrRef] = None
    cc: Optional[StrOrRef] = None
    bcc: Optional[StrOrRef] = None
    body: Optional[StrOrRef] = None
    header: Optional[ListOrRef[str]] = None


@dataclass
class EmailQueryFilterOperator(Model):
    operator: Operator
    conditions: List[EmailQueryFilter]


EmailQueryFilter = Union[EmailQueryFilterCondition, EmailQueryFilterOperator]
