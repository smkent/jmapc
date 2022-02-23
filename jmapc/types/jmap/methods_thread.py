from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config

from ... import constants
from .methods import JMAPMethod, JMAPResponse
from .models import JMAPThread


@dataclass
class JMAPThreadGet(JMAPMethod):
    @property
    def name(self) -> str:
        return "Thread/get"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    ids: List[str]


@dataclass
class JMAPThreadGetResponse(JMAPResponse):
    data: List[JMAPThread] = field(metadata=config(field_name="list"))
