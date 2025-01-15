from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Union

from dataclasses_json import DataClassJsonMixin, config

from ..serializer import Model, datetime_decode, datetime_encode
from .models import Operator


@dataclass
class EmailSubmission(Model):
    id: Optional[str] = field(metadata=config(field_name="id"), default=None)
    identity_id: Optional[str] = None
    email_id: Optional[str] = None
    thread_id: Optional[str] = None
    envelope: Optional[Envelope] = None
    send_at: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    undo_status: Optional[UndoStatus] = None
    delivery_status: Optional[dict[str, DeliveryStatus]] = None
    dsn_blob_ids: Optional[list[str]] = None
    mdn_blob_ids: Optional[list[str]] = None


@dataclass
class Envelope(Model):
    mail_from: Optional[Address] = None
    rcpt_to: Optional[list[Address]] = None


@dataclass
class Address(DataClassJsonMixin):
    email: Optional[str] = None
    parameters: Optional[dict[str, str]] = None


class UndoStatus(Enum):
    PENDING = "pending"
    FINAL = "final"
    CANCELED = "canceled"


@dataclass
class DeliveryStatus(Model):
    smtp_reply: str
    delivered: Delivered
    displayed: Displayed


class Delivered(Enum):
    QUEUED = "queued"
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class Displayed(Enum):
    UNKNOWN = "unknown"
    YES = "yes"


@dataclass
class EmailSubmissionQueryFilterCondition(Model):
    identity_ids: Optional[list[str]] = None
    email_ids: Optional[list[str]] = None
    thread_ids: Optional[list[str]] = None
    undo_status: Optional[UndoStatus] = None
    before: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    after: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )


@dataclass
class EmailSubmissionQueryFilterOperator(Model):
    operator: Operator
    conditions: list[EmailSubmissionQueryFilter]


EmailSubmissionQueryFilter = Union[
    EmailSubmissionQueryFilterCondition, EmailSubmissionQueryFilterOperator
]
