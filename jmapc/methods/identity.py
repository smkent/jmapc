from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import config

from .. import constants
from ..models import Identity
from ..serializer import ListOrRef
from .methods import Get, GetResponse


@dataclass
class IdentityGet(Get):
    @classmethod
    def name(cls) -> str:
        return "Identity/get"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_SUBMISSION])

    ids: Optional[ListOrRef[str]] = None


@dataclass
class IdentityGetResponse(GetResponse):
    data: List[Identity] = field(metadata=config(field_name="list"))
