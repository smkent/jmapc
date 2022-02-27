from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from dataclasses_json import DataClassJsonMixin, config

from ..serializer import Model, datetime_decode, datetime_encode


@dataclass
class EmailSubmission(Model):
    id: Optional[str] = field(metadata=config(field_name="Id"), default=None)
    identity_id: Optional[str] = None
    email_id: Optional[str] = None
    thread_id: Optional[str] = None
    envelope: Optional[Envelope] = None
    send_at: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    undo_status: Optional[UndoStatus] = None
    dsn_blob_ids: Optional[List[str]] = None
    mdn_blob_ids: Optional[List[str]] = None


@dataclass
class Envelope(Model):
    mail_from: Optional[Address] = None
    rcpt_to: Optional[List[Address]] = None


@dataclass
class Address(DataClassJsonMixin):
    email: Optional[str] = None
    parameters: Optional[Dict[str, str]] = None


class UndoStatus:
    PENDING = "pending"
    FINAL = "final"
    CANCELED = "canceled"


@dataclass
class DeliveryStatus(Model):
    smtp_reply: Optional[str] = None
    delivered: Optional[Delivered] = None
    displayed: Optional[Displayed] = None


class Delivered:
    QUEUED = "queued"
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class Displayed:
    UNKNOWN = "unknown"
    YES = "yes"
