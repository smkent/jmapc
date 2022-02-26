from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type

from .serializer import Model

__all__ = ["Error", "ServerFail"]


@dataclass
class Error(Model):
    type: str

    @staticmethod
    def _errors_map() -> Dict[str, Type[Error]]:
        return {
            "invalidArguments": InvalidArguments,
            "serverFail": ServerFail,
        }

    @classmethod
    def from_dict(cls, *args: Any, **kwargs: Any) -> Error:
        res = super().from_dict(*args, **kwargs)
        if cls == Error:
            errors_map = cls._errors_map()
            if res.type in errors_map:
                return errors_map[res.type].from_dict(*args, **kwargs)
            return res
        return res


@dataclass
class InvalidArguments(Error):
    arguments: List[str]


@dataclass
class ServerFail(Error):
    description: Optional[str]
