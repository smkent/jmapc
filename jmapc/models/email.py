from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union, Final

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


class EmailProperties:
    """Property keys of an email object.

    References:
        https://jmap.io/spec-mail.html#properties-of-the-email-object
    """

    ID: Final[str] = "id"
    BLOB_ID: Final[str] = "blobId"
    THREAD_ID: Final[str] = "threadId"
    MAILBOX_IDS: Final[str] = "mailboxIds"
    KEYWORDS: Final[str] = "keywords"
    SIZE: Final[str] = "size"
    RECEIVED_AT: Final[str] = "receivedAt"
    MESSAGE_ID: Final[str] = "messageId"
    IN_REPLY_TO: Final[str] = "inReplyTo"
    REFERENCES: Final[str] = "references"
    SENDER: Final[str] = "sender"
    FROM: Final[str] = "from"
    TO: Final[str] = "to"
    CC: Final[str] = "cc"
    BCC: Final[str] = "bcc"
    REPLY_TO: Final[str] = "replyTo"
    SUBJECT: Final[str] = "subject"
    SENT_AT: Final[str] = "sentAt"
    BODY_STRUCTURE: Final[str] = "bodyStructure"
    BODY_VALUES: Final[str] = "bodyValues"
    TEXT_BODY: Final[str] = "textBody"
    HTML_BODY: Final[str] = "htmlBody"
    ATTACHMENTS: Final[str] = "attachments"
    HAS_ATTACHMENT: Final[str] = "hasAttachment"
    PREVIEW: Final[str] = "preview"


class EmailBodyPartProperties:
    """Property keys of an email bodypart object.

    References:
        https://jmap.io/spec-mail.html#properties-of-the-email-object
    """

    PART_ID: Final[str] = "partId"
    BLOB_ID: Final[str] = "blobId"
    SIZE: Final[str] = "size"
    HEADERS: Final[str] = "headers"
    NAME: Final[str] = "name"
    TYPE: Final[str] = "type"
    CHARSET: Final[str] = "charset"
    DISPOSITION: Final[str] = "disposition"
    CID: Final[str] = "cid"
    LANGUAGE: Final[str] = "language"
    LOCATION: Final[str] = "location"
    SUB_PARTS: Final[str] = "subParts"


EmailQueryFilter = Union[EmailQueryFilterCondition, EmailQueryFilterOperator]
