from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config

from .. import constants
from ..models import Identity
from .methods import Get, GetResponse


@dataclass
class IdentityGet(Get):
    @classmethod
    def name(cls) -> str:
        return "Identity/get"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_SUBMISSION])


@dataclass
class IdentityGetResponse(GetResponse):
    data: List[Identity] = field(metadata=config(field_name="list"))
