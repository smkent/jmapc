from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import config

from .. import constants
from ..models import Identity, ListOrRef
from .base import Changes, ChangesResponse, Get, GetResponse, Set, SetResponse


class IdentityBase:
    method_namespace: Optional[str] = "Identity"
    using = set([constants.JMAP_URN_SUBMISSION])


@dataclass
class IdentityChanges(IdentityBase, Changes):
    pass


@dataclass
class IdentityChangesResponse(IdentityBase, ChangesResponse):
    pass


@dataclass
class IdentityGet(IdentityBase, Get):
    ids: Optional[ListOrRef[str]] = None


@dataclass
class IdentityGetResponse(IdentityBase, GetResponse):
    data: List[Identity] = field(metadata=config(field_name="list"))


@dataclass
class IdentitySet(IdentityBase, Set):
    create: Optional[Dict[str, Identity]] = None


@dataclass
class IdentitySetResponse(IdentityBase, SetResponse):
    created: Optional[Dict[str, Optional[Identity]]]
    updated: Optional[Dict[str, Optional[Identity]]]
