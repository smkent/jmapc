from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import config

from .. import constants
from ..models import Identity, ListOrRef
from .base import Get, GetResponse


@dataclass
class IdentityGet(Get):
    name = "Identity/get"
    using = set([constants.JMAP_URN_SUBMISSION])

    ids: Optional[ListOrRef[str]] = None


@dataclass
class IdentityGetResponse(GetResponse):
    data: List[Identity] = field(metadata=config(field_name="list"))
