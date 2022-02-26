from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config

from .. import constants
from .methods import JMAPGet, JMAPGetResponse
from .models import JMAPIdentity


@dataclass
class JMAPIdentityGet(JMAPGet):
    @classmethod
    def name(cls) -> str:
        return "Identity/get"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_SUBMISSION])


@dataclass
class JMAPIdentityGetResponse(JMAPGetResponse):
    data: List[JMAPIdentity] = field(metadata=config(field_name="list"))
