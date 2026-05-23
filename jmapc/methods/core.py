from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from jmapc import constants

from .base import Method, Response


class CoreBase:
    method_namespace: ClassVar[str | None] = "Core"
    using: ClassVar[set[str]] = {constants.JMAP_URN_CORE}


class EchoMethod:
    method_type: str | None = "echo"


@dataclass
class CoreEcho(CoreBase, EchoMethod, Method):
    def to_dict(self, *_args: Any, **_kwargs: Any) -> dict[str, Any]:
        return self.data or {}

    data: dict[str, Any] | None = None


@dataclass
class CoreEchoResponse(CoreBase, EchoMethod, Response):
    data: dict[str, Any] | None = None

    @classmethod
    def from_dict(
        cls, kvs: Any, *_args: Any, **_kwargs: Any
    ) -> CoreEchoResponse:
        return CoreEchoResponse(data=kvs)
