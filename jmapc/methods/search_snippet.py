from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from dataclasses_json import config

from jmapc import constants
from jmapc.models import EmailQueryFilter, ListOrRef, SearchSnippet, TypeOrRef

from .base import Get, GetResponseWithoutState


class SearchSnippetBase:
    method_namespace: ClassVar[str | None] = "SearchSnippet"
    using: ClassVar[set[str]] = {constants.JMAP_URN_MAIL}


@dataclass
class SearchSnippetGet(SearchSnippetBase, Get):
    ids: ListOrRef[str] | None = field(
        metadata=config(field_name="emailIds"), default=None
    )
    filter: TypeOrRef[EmailQueryFilter] | None = None


@dataclass
class SearchSnippetGetResponse(SearchSnippetBase, GetResponseWithoutState):
    data: list[SearchSnippet] = field(metadata=config(field_name="list"))
