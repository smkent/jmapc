from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from dataclasses_json import config

from jmapc.serializer import Model, datetime_decode, datetime_encode


class MaskedEmailState(Enum):
    PENDING = "pending"
    ENABLED = "enabled"
    DISABLED = "disabled"
    DELETED = "deleted"


@dataclass
class MaskedEmail(Model):
    id: str | None = None
    email: str | None = None
    state: MaskedEmailState | None = None
    for_domain: str | None = None
    description: str | None = None
    last_message_at: datetime | None = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    created_at: datetime | None = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    created_by: str | None = None
    url: str | None = None
    email_prefix: str | None = None
