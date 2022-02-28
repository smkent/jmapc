from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .. import constants
from .base import Method, Response


@dataclass
class CoreEcho(Method):
    name = "Core/echo"
    using = set([constants.JMAP_URN_CORE])

    def to_dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return self.data or dict()

    data: Optional[Dict[str, Any]] = None


@dataclass
class CoreEchoResponse(Response):
    name = "Core/echo"
    data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(
        cls, kvs: Any, *args: Any, **kwargs: Any
    ) -> CoreEchoResponse:
        return CoreEchoResponse(data=kvs)
