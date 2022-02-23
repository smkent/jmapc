from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, config


@dataclass
class JMAPMethodBase(DataClassJsonMixin):
    account_id: str = field(metadata=config(field_name="accountId"))


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
