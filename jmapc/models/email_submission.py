from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from dataclasses_json import DataClassJsonMixin, config

from jmapc.serializer import Model, datetime_decode, datetime_encode

from .models import Operator


@dataclass
class EmailSubmission(Model):
    id: str | None = field(metadata=config(field_name="id"), default=None)
    identity_id: str | None = None
    email_id: str | None = None
    thread_id: str | None = None
    envelope: Envelope | None = None
    send_at: datetime | None = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    undo_status: UndoStatus | None = None
    delivery_status: dict[str, DeliveryStatus] | None = None
    dsn_blob_ids: list[str] | None = None
    mdn_blob_ids: list[str] | None = None


@dataclass
class Envelope(Model):
    mail_from: Address | None = None
    rcpt_to: list[Address] | None = None


@dataclass
class Address(DataClassJsonMixin):
    email: str | None = None
    parameters: dict[str, str] | None = None


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
    identity_ids: list[str] | None = None
    email_ids: list[str] | None = None
    thread_ids: list[str] | None = None
    undo_status: UndoStatus | None = None
    before: datetime | None = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    after: datetime | None = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )


@dataclass
class EmailSubmissionQueryFilterOperator(Model):
    operator: Operator
    conditions: list[EmailSubmissionQueryFilter]


EmailSubmissionQueryFilter = (
    EmailSubmissionQueryFilterCondition | EmailSubmissionQueryFilterOperator
)
