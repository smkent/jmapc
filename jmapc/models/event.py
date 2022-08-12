import json
from dataclasses import dataclass, field
from typing import Dict, Optional

import sseclient
from dataclasses_json import config

from ..serializer import Model


@dataclass
class TypeState(Model):
    calendar_event: Optional[str] = field(
        metadata=config(field_name="CalendarEvent"), default=None
    )
    mailbox: Optional[str] = field(
        metadata=config(field_name="Mailbox"), default=None
    )
    email: Optional[str] = field(
        metadata=config(field_name="Email"), default=None
    )
    email_delivery: Optional[str] = field(
        metadata=config(field_name="EmailDelivery"), default=None
    )
    thread: Optional[str] = field(
        metadata=config(field_name="Thread"), default=None
    )


@dataclass
class StateChange(Model):
    changed: Dict[str, TypeState]
    type: Optional[str] = None


@dataclass
class Event(Model):
    id: str
    data: StateChange

    @classmethod
    def load_from_sseclient_event(cls, event: sseclient.Event) -> "Event":
        data = json.loads(event.data)
        return cls.from_dict({"id": event.id, "data": data})
