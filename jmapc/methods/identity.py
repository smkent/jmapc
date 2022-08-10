from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import config

from .. import constants
from ..models import Identity, ListOrRef
from .base import Changes, ChangesResponse, Get, GetResponse, Set, SetResponse


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


@dataclass
class IdentitySet(Set):
    name = "Identity/set"
    using = set([constants.JMAP_URN_SUBMISSION])

    create: Optional[Dict[str, Identity]] = None


@dataclass
class IdentitySetResponse(SetResponse):
    name = "Identity/set"

    created: Optional[Dict[str, Optional[Identity]]]
    updated: Optional[Dict[str, Optional[Identity]]]
