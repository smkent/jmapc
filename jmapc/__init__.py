import logging

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
    Mailbox,
    Operator,
    Thread,
    ThreadEmail,
)
from .ref import ResultReference
from .serializer import ListOrRef, StrOrRef

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

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
