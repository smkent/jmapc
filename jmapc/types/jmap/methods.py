from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin, config

from ... import constants
from .methods_identity import JMAPIdentity


class JMAPMethod(DataClassJsonMixin):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def using(self) -> set[str]:
        pass


@dataclass
class JMAPIdentityGet(JMAPMethod):
    @property
    def name(self) -> str:
        return "Identity/get"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_SUBMISSION])

    account_id: str = field(metadata=config(field_name="accountId"))


class JMAPResponse(DataClassJsonMixin):
    pass


@dataclass
class JMAPIdentityGetResponse(JMAPResponse):
    account_id: str = field(metadata=config(field_name="accountId"))
    data: List[JMAPIdentity] = field(metadata=config(field_name="list"))
