from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import config

from ..methods.base import Get, GetResponse, Set, SetResponse
from .maskedemail_models import MaskedEmail

URN = "https://www.fastmail.com/dev/maskedemail"


class MaskedEmailBase:
    method_namespace: Optional[str] = "MaskedEmail"
    using = {URN}


@dataclass
class MaskedEmailGet(MaskedEmailBase, Get):
    pass


@dataclass
class MaskedEmailGetResponse(MaskedEmailBase, GetResponse):
    data: list[MaskedEmail] = field(metadata=config(field_name="list"))


@dataclass
class MaskedEmailSet(MaskedEmailBase, Set):
    pass


@dataclass
class MaskedEmailSetResponse(MaskedEmailBase, SetResponse):
    created: Optional[dict[str, Optional[MaskedEmail]]]
    updated: Optional[dict[str, Optional[MaskedEmail]]]
