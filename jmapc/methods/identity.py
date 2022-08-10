from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import config

from .. import constants
from ..models import Identity, ListOrRef
from .base import Changes, ChangesResponse, Get, GetResponse


@dataclass
class IdentityChanges(Changes):
    name = "Identity/changes"
    using = set([constants.JMAP_URN_SUBMISSION])


@dataclass
class IdentityChangesResponse(ChangesResponse):
    name = "Identity/changes"


@dataclass
class IdentityGet(Get):
    name = "Identity/get"
    using = set([constants.JMAP_URN_SUBMISSION])

    ids: Optional[ListOrRef[str]] = None


@dataclass
class IdentityGetResponse(GetResponse):
    name = "Identity/get"

    data: List[Identity] = field(metadata=config(field_name="list"))
