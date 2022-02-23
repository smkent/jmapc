from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, config

from ... import constants
from .methods import JMAPMethod, JMAPResponse
from .models import JMAPMailbox


@dataclass
class JMAPMailboxQuery(JMAPMethod):
    @property
    def name(self) -> str:
        return "Mailbox/query"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    filter: Optional[JMAPMailboxQueryFilter]


@dataclass
class JMAPMailboxQueryResponse(JMAPResponse):
    ids: List[str]


@dataclass
class JMAPMailboxQueryFilter(DataClassJsonMixin):
    name: Optional[str] = None
    role: Optional[str] = None
    parent_id: Optional[str] = field(
        metadata=config(field_name="parentId"), default=None
    )


@dataclass
class JMAPMailboxGet(JMAPMethod):
    @property
    def name(self) -> str:
        return "Mailbox/get"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    ids: List[str]


@dataclass
class JMAPMailboxGetResponse(JMAPResponse):
    data: List[JMAPMailbox] = field(metadata=config(field_name="list"))
