from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ..serializer import Model
from .models import EmailAddress


@dataclass
class Identity(Model):
    id: str
    name: str
    email: str
    replyTo: Optional[str]
    bcc: Optional[List[EmailAddress]]
    textSignature: Optional[str]
    htmlSignature: Optional[str]
    mayDelete: bool
