from . import errors, methods
from .client import Client
from .errors import Error
from .models import (
    Comparator,
    Email,
    EmailAddress,
    EmailBodyPart,
    EmailBodyValue,
    EmailHeader,
    Identity,
    ListOrRef,
    Mailbox,
    Operator,
    StrOrRef,
    Thread,
    ThreadEmail,
)
from .ref import ResultReference

__all__ = [
    "Client",
    "Comparator",
    "Email",
    "EmailAddress",
    "EmailBodyPart",
    "EmailBodyValue",
    "EmailHeader",
    "Error",
    "Identity",
    "ListOrRef",
    "Mailbox",
    "Operator",
    "ResultReference",
    "StrOrRef",
    "Thread",
    "ThreadEmail",
    "errors",
    "methods",
]
