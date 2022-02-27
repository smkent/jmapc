from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .base import MethodWithAccount, ResponseWithAccount


@dataclass
class CustomMethod(MethodWithAccount):
    def __post_init__(self) -> None:
        self.name = "Custom/method"
        self.using = set()

    def to_dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return self.data or dict()

    data: Optional[Dict[str, Any]] = None


@dataclass
class CustomResponse(ResponseWithAccount):
    data: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        if self.data and "accountId" in self.data:
            del self.data["accountId"]

    @classmethod
    def from_dict(cls, kvs: Any, *args: Any, **kwargs: Any) -> CustomResponse:
        account_id = kvs.pop("accountId")
        return CustomResponse(account_id=account_id, data=kvs)
