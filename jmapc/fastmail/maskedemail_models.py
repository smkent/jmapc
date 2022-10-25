from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from dataclasses_json import config

from ..serializer import Model, datetime_decode, datetime_encode


class MaskedEmailState(Enum):
    PENDING = "pending"
    ENABLED = "enabled"
    DISABLED = "disabled"
    DELETED = "deleted"


@dataclass
class MaskedEmail(Model):
    id: Optional[str] = None
    email: Optional[str] = None
    for_domain: Optional[str] = None
    description: Optional[str] = None
    last_message_at: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    created_at: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    created_by: Optional[str] = None
    url: Optional[str] = None
    email_prefix: Optional[str] = None
