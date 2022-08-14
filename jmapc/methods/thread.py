from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import config

from .. import constants
from ..models import Thread
from .base import Changes, ChangesResponse, Get, GetResponse


class ThreadBase:
    method_namespace: Optional[str] = "Thread"
    using = set([constants.JMAP_URN_MAIL])


@dataclass
class ThreadChanges(ThreadBase, Changes):
    pass


@dataclass
class ThreadChangesResponse(ThreadBase, ChangesResponse):
    pass


@dataclass
class ThreadGet(ThreadBase, Get):
    pass


@dataclass
class ThreadGetResponse(ThreadBase, GetResponse):
    data: List[Thread] = field(metadata=config(field_name="list"))
