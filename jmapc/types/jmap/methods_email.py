from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, config

from ... import constants
from .methods import JMAPMethod, JMAPResponse
from .models import JMAPEmail


@dataclass
class JMAPEmailQuery(JMAPMethod):
    @property
    def name(self) -> str:
        return "Email/query"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    filter: Optional[JMAPEmailQueryFilter]


@dataclass
class JMAPEmailQueryResponse(JMAPResponse):
    ids: List[str]


@dataclass
class JMAPEmailQueryFilter(DataClassJsonMixin):
    in_mailbox: str = field(metadata=config(field_name="inMailbox"))


@dataclass
class JMAPEmailGet(JMAPMethod):
    @property
    def name(self) -> str:
        return "Email/get"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_MAIL])

    ids: List[str]


@dataclass
class JMAPEmailGetResponse(JMAPResponse):
    data: List[JMAPEmail] = field(metadata=config(field_name="list"))
