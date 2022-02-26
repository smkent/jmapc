from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config

from .. import constants
from .methods import JMAPGet, JMAPGetResponse
from .models import JMAPThread


@dataclass
class JMAPThreadGet(JMAPGet):
    @classmethod
    def name(cls) -> str:
        return "Thread/get"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])


@dataclass
class JMAPThreadGetResponse(JMAPGetResponse):
    data: List[JMAPThread] = field(metadata=config(field_name="list"))
