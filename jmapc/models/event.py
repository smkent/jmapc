import json
from dataclasses import dataclass, field

import sseclient
from dataclasses_json import config

from jmapc.serializer import Model


@dataclass
class TypeState(Model):
    calendar_event: str | None = field(
        metadata=config(field_name="CalendarEvent"), default=None
    )
    mailbox: str | None = field(
        metadata=config(field_name="Mailbox"), default=None
    )
    email: str | None = field(
        metadata=config(field_name="Email"), default=None
    )
    email_delivery: str | None = field(
        metadata=config(field_name="EmailDelivery"), default=None
    )
    thread: str | None = field(
        metadata=config(field_name="Thread"), default=None
    )


@dataclass
class StateChange(Model):
    changed: dict[str, TypeState]
    type: str | None = None


@dataclass
class Event(Model):
    id: str | None
    data: StateChange

    @classmethod
    def load_from_sseclient_event(cls, event: sseclient.Event) -> "Event":
        data = json.loads(event.data)
        return cls.from_dict({"id": event.id, "data": data})
