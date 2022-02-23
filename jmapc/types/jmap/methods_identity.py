from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config

from ... import constants
from .methods import JMAPMethod, JMAPResponse
from .models import JMAPIdentity


@dataclass
class JMAPIdentityGet(JMAPMethod):
    @property
    def name(self) -> str:
        return "Identity/get"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_SUBMISSION])


@dataclass
class JMAPIdentityGetResponse(JMAPResponse):
    data: List[JMAPIdentity] = field(metadata=config(field_name="list"))
