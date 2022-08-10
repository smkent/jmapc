from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config

from .. import constants
from ..models import Thread
from .base import Changes, ChangesResponse, Get, GetResponse


@dataclass
class ThreadChanges(Changes):
    name = "Thread/changes"
    using = set([constants.JMAP_URN_MAIL])


@dataclass
class ThreadChangesResponse(ChangesResponse):
    name = "Thread/changes"


@dataclass
class ThreadGet(Get):
    name = "Thread/get"
    using = set([constants.JMAP_URN_MAIL])


@dataclass
class ThreadGetResponse(GetResponse):
    name = "Thread/get"

    data: List[Thread] = field(metadata=config(field_name="list"))
