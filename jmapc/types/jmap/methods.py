from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field

from typing import Optional

from ..util import JsonDataClass


@dataclass
class JMAPMethodBase(JsonDataClass):
    pass


@dataclass
class JMAPMethodAccountID(JMAPMethodBase):
    account_id: Optional[str] = field(init=False, default=None)


class JMAPMethod(JMAPMethodAccountID):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def using(self) -> set[str]:
        pass


@dataclass
class JMAPResponse(JMAPMethodBase):
    account_id: Optional[str]
