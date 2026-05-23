from __future__ import annotations

from dataclasses import dataclass

from jmapc.serializer import Model

from .models import EmailAddress


@dataclass
class Identity(Model):
    name: str
    email: str
    reply_to: str | None
    bcc: list[EmailAddress] | None
    text_signature: str | None
    html_signature: str | None
    may_delete: bool
    id: str | None = None
