from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config

from ... import constants
from .methods import JMAPGet, JMAPGetResponse
from .models import JMAPThread


@dataclass
class JMAPThreadGet(JMAPGet):
    @property
    def name(self) -> str:
        return "Thread/get"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_MAIL])


@dataclass
class JMAPThreadGetResponse(JMAPGetResponse):
    data: List[JMAPThread] = field(metadata=config(field_name="list"))
