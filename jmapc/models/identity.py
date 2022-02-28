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
    reply_to: Optional[str]
    bcc: Optional[List[EmailAddress]]
    text_signature: Optional[str]
    html_signature: Optional[str]
    may_delete: bool
