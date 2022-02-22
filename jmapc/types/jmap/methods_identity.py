from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin


@dataclass
class JMAPIdentity(DataClassJsonMixin):
    id: str
    name: str
    email: str
    replyTo: Optional[str]
    bcc: Optional[List[JMAPIdentityBCC]]
    textSignature: Optional[str]
    htmlSignature: Optional[str]
    mayDelete: bool


@dataclass
class JMAPIdentityBCC(DataClassJsonMixin):
    name: Optional[str]
    email: str
