import functools
from dataclasses import dataclass, field
from typing import Optional, Set

from dataclasses_json import CatchAll, Undefined, config, dataclass_json

from . import constants
from .serializer import Model


@dataclass
class Session(Model):
    username: str
    api_url: str
    download_url: str
    upload_url: str
    event_source_url: str
    primary_accounts: "SessionPrimaryAccount"
    capabilities: "SessionCapabilities"


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class SessionCapabilities(Model):
    # dataclasses_json.CatchAll Currently does not work with
    # from __future__ import annotations
    core: "SessionCapabilitiesCore" = field(
        metadata=config(field_name=constants.JMAP_URN_CORE)
    )
    extensions: CatchAll = field(default_factory=dict)

    @functools.cached_property
    def urns(self) -> Set[str]:
        return set(self.to_dict().keys())


@dataclass
class SessionCapabilitiesCore(Model):
    max_size_upload: int
    max_concurrent_upload: int
    max_size_request: int
    max_concurrent_requests: int
    max_calls_in_request: int
    max_objects_in_get: int
    max_objects_in_set: int
    collation_algorithms: Set[str]


@dataclass
class SessionPrimaryAccount(Model):
    core: Optional[str] = field(
        metadata=config(field_name=constants.JMAP_URN_CORE), default=None
    )
    mail: Optional[str] = field(
        metadata=config(field_name=constants.JMAP_URN_MAIL), default=None
    )
    submission: Optional[str] = field(
        metadata=config(field_name=constants.JMAP_URN_SUBMISSION), default=None
    )
