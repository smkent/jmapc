from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

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
    data: List[MaskedEmail] = field(metadata=config(field_name="list"))


@dataclass
class MaskedEmailSet(MaskedEmailBase, Set):
    pass


@dataclass
class MaskedEmailSetResponse(MaskedEmailBase, SetResponse):
    created: Optional[Dict[str, Optional[MaskedEmail]]]
    updated: Optional[Dict[str, Optional[MaskedEmail]]]
