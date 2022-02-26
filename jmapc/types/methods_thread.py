from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config

from .. import constants
from .methods import Get, GetResponse
from .models import Thread


@dataclass
class ThreadGet(Get):
    @classmethod
    def name(cls) -> str:
        return "Thread/get"

    @classmethod
    def using(cls) -> set[str]:
        return set([constants.JMAP_URN_MAIL])


@dataclass
class ThreadGetResponse(GetResponse):
    data: List[Thread] = field(metadata=config(field_name="list"))
