from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from dataclasses_json import config

from jmapc import constants
from jmapc.models import Identity, ListOrRef

from .base import Changes, ChangesResponse, Get, GetResponse, Set, SetResponse


class IdentityBase:
    method_namespace: ClassVar[str | None] = "Identity"
    using: ClassVar[set[str]] = {constants.JMAP_URN_SUBMISSION}


@dataclass
class IdentityChanges(IdentityBase, Changes):
    pass


@dataclass
class IdentityChangesResponse(IdentityBase, ChangesResponse):
    pass


@dataclass
class IdentityGet(IdentityBase, Get):
    ids: ListOrRef[str] | None = None


@dataclass
class IdentityGetResponse(IdentityBase, GetResponse):
    data: list[Identity] = field(metadata=config(field_name="list"))


@dataclass
class IdentitySet(IdentityBase, Set):
    create: dict[str, Identity] | None = None


@dataclass
class IdentitySetResponse(IdentityBase, SetResponse):
    created: dict[str, Identity | None] | None
    updated: dict[str, Identity | None] | None
