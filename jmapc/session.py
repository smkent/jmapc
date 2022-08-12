from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses_json import config

from . import constants
from .serializer import Model


@dataclass
class Session(Model):
    username: str
    api_url: str = field(metadata=config(field_name="apiUrl"))
    event_source_url: str = field(metadata=config(field_name="eventSourceUrl"))
    primary_accounts: SessionPrimaryAccount = field(
        metadata=config(field_name="primaryAccounts")
    )


@dataclass
class SessionPrimaryAccount(Model):
    core: str = field(metadata=config(field_name=constants.JMAP_URN_CORE))
    mail: str = field(metadata=config(field_name=constants.JMAP_URN_MAIL))
    submission: str = field(
        metadata=config(field_name=constants.JMAP_URN_SUBMISSION)
    )
