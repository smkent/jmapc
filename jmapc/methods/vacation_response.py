from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import config

from .. import constants
from ..models import VacationResponse
from .base import Get, GetResponseWithoutState, Set, SetResponse


class VacationResponseBase:
    method_namespace: Optional[str] = "VacationResponse"
    using = set([constants.JMAP_URN_VACATION_RESPONSE])


@dataclass
class VacationResponseGet(VacationResponseBase, Get):
    ids: Optional[List[str]] = None


@dataclass
class VacationResponseGetResponse(
    VacationResponseBase, GetResponseWithoutState
):
    data: List[VacationResponse] = field(metadata=config(field_name="list"))


@dataclass
class VacationResponseSet(VacationResponseBase, Set):
    create: Optional[Dict[str, VacationResponse]] = None


@dataclass
class VacationResponseSetResponse(VacationResponseBase, SetResponse):
    created: Optional[Dict[str, Optional[VacationResponse]]]
    updated: Optional[Dict[str, Optional[VacationResponse]]]
