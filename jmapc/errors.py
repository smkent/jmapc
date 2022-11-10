from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, cast

from .serializer import Model

__all__ = ["Error", "ServerFail"]


class ErrorCollector(Model):
    error_types: Dict[str, Type[Error]] = {}

    @classmethod
    def __init_subclass__(cls) -> None:
        error_class = cast(Type["Error"], cls)
        type_attr = getattr(error_class, "_type", None)
        if type_attr:
            ErrorCollector.error_types[type_attr] = error_class


@dataclass
class Error(ErrorCollector):
    type: str = ""

    def __post_init__(self) -> None:
        type_attr = getattr(self, "_type", None)
        if type_attr:
            self.type = type_attr

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
    _type = "accountNotFound"


@dataclass
class AccountNotSupportedByMethod(Error):
    _type = "accountNotSupportedByMethod"


@dataclass
class AccountReadOnly(Error):
    _type = "accountReadOnly"


@dataclass
class CannotCalculateChanges(Error):
    _type = "cannotCalculateChanges"


@dataclass
class InvalidArguments(Error):
    _type = "invalidArguments"
    arguments: Optional[List[str]] = None
    description: Optional[str] = None


@dataclass
class InvalidResultReference(Error):
    _type = "invalidResultReference"


@dataclass
class Forbidden(Error):
    _type = "forbidden"


@dataclass
class RequestTooLarge(Error):
    _type = "requestTooLarge"


@dataclass
class ServerFail(Error):
    _type = "serverFail"
    description: Optional[str] = None


@dataclass
class ServerPartialFail(Error):
    _type = "serverPartialFail"


@dataclass
class ServerUnavailable(Error):
    _type = "serverUnavailable"


@dataclass
class UnknownMethod(Error):
    _type = "unknownMethod"


@dataclass
class UnsupportedFilter(Error):
    _type = "UnsupportedFilter"
