from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass

from ..util import JsonDataClass


@dataclass
class JMAPMethodBase(JsonDataClass):
    account_id: str


class JMAPMethod(JMAPMethodBase):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def using(self) -> set[str]:
        pass


class JMAPResponse(JMAPMethodBase):
    pass
