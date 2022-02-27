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
            "accountNotFound": AccountNotFound,
            "accountNotSupportedByMethod": AccountNotSupportedByMethod,
            "accountReadOnly": AccountReadOnly,
            "invalidArguments": InvalidArguments,
            "invalidResultReference": InvalidResultReference,
            "forbidden": Forbidden,
            "serverFail": ServerFail,
            "serverPartialFail": ServerPartialFail,
            "serverUnavailable": ServerUnavailable,
            "unknownMethod": UnknownMethod,
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
class AccountNotFound(Error):
    pass


@dataclass
class AccountNotSupportedByMethod(Error):
    pass


@dataclass
class AccountReadOnly(Error):
    pass


@dataclass
class InvalidArguments(Error):
    arguments: Optional[List[str]] = None
    description: Optional[str] = None


@dataclass
class InvalidResultReference(Error):
    pass


@dataclass
class Forbidden(Error):
    pass


@dataclass
class ServerFail(Error):
    description: Optional[str] = None


@dataclass
class ServerPartialFail(Error):
    pass


@dataclass
class ServerUnavailable(Error):
    pass


@dataclass
class UnknownMethod(Error):
    pass
