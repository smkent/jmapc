from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, cast

from .serializer import Model

__all__ = ["Error", "ServerFail"]


class ErrorCollector(Model):
    error_types: Dict[str, Type[Error]] = {}

    @classmethod
    def __init_subclass__(cls) -> None:
        error_class = cast(Type["Error"], cls)
        type_attr = getattr(error_class, "type", None)
        if type_attr:
            ErrorCollector.error_types[type_attr] = error_class


@dataclass
class Error(ErrorCollector):
    type: str

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _errors_map() -> Dict[str, Type[Error]]:
        errors_map: Dict[str, Type[Error]] = dict()
        for cls in Error.__subclasses__():
            errors_map[cls.type] = cls
        return errors_map

    @classmethod
    def from_dict(cls, *args: Any, **kwargs: Any) -> Error:
        res = super().from_dict(*args, **kwargs)
        if cls == Error:
            res_type = ErrorCollector.error_types.get(res.type)
            if res_type:
                return res_type.from_dict(*args, **kwargs)
            return res
        return res


@dataclass
class AccountNotFound(Error):
    type = "accountNotFound"


@dataclass
class AccountNotSupportedByMethod(Error):
    type = "accountNotSupportedByMethod"


@dataclass
class AccountReadOnly(Error):
    type = "accountReadOnly"


@dataclass
class InvalidArguments(Error):
    type = "invalidArguments"
    arguments: Optional[List[str]] = None
    description: Optional[str] = None


@dataclass
class InvalidResultReference(Error):
    type = "invalidResultReference"


@dataclass
class Forbidden(Error):
    type = "forbidden"


@dataclass
class ServerFail(Error):
    type = "serverFail"
    description: Optional[str] = None


@dataclass
class ServerPartialFail(Error):
    type = "serverPartialFail"


@dataclass
class ServerUnavailable(Error):
    type = "serverUnavailable"


@dataclass
class UnknownMethod(Error):
    type = "unknownMethod"
