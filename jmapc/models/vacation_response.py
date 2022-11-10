from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import config

from ..serializer import Model, datetime_decode, datetime_encode


@dataclass
class VacationResponse(Model):
    id: str
    is_enabled: bool
    from_date: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    to_date: Optional[datetime] = field(
        default=None,
        metadata=config(encoder=datetime_encode, decoder=datetime_decode),
    )
    subject: Optional[str] = None
    text_body: Optional[str] = None
    html_body: Optional[str] = None
