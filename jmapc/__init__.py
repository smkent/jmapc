from . import errors, methods
from .client import Client
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
    "Comparator",
    "Email",
    "EmailAddress",
    "EmailBodyPart",
    "EmailBodyValue",
    "EmailHeader",
    "Identity",
    "Client",
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
