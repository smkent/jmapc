from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from dataclasses_json import config

from jmapc import constants
from jmapc.models import Thread

from .base import Changes, ChangesResponse, Get, GetResponse


class ThreadBase:
    method_namespace: ClassVar[str | None] = "Thread"
    using: ClassVar[set[str]] = {constants.JMAP_URN_MAIL}


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
    data: list[Thread] = field(metadata=config(field_name="list"))
