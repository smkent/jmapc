from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .. import constants
from .base import Method, Response


class CoreBase:
    method_namespace: Optional[str] = "Core"
    using = {constants.JMAP_URN_CORE}


class EchoMethod:
    method_type: Optional[str] = "echo"


@dataclass
class CoreEcho(CoreBase, EchoMethod, Method):
    def to_dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return self.data or dict()

    data: Optional[dict[str, Any]] = None


@dataclass
class CoreEchoResponse(CoreBase, EchoMethod, Response):
    data: Optional[dict[str, Any]] = None

    @classmethod
    def from_dict(
        cls, kvs: Any, *args: Any, **kwargs: Any
    ) -> CoreEchoResponse:
        return CoreEchoResponse(data=kvs)
