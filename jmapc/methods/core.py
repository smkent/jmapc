from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .base import Method, Response


@dataclass
class CoreEcho(Method):
    @classmethod
    def name(cls) -> str:
        return "Core/echo"

    @classmethod
    def using(cls) -> set[str]:
        return set()

    def to_dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return self.data or dict()

    data: Optional[Dict[str, Any]] = None


@dataclass
class CoreEchoResponse(Response):
    data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(
        cls, kvs: Any, *args: Any, **kwargs: Any
    ) -> CoreEchoResponse:
        return CoreEchoResponse(data=kvs)
