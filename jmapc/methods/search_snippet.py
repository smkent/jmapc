from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import config

from .. import constants
from ..models import EmailQueryFilter, ListOrRef, SearchSnippet, TypeOrRef
from .base import Get, GetResponseWithoutState


class SearchSnippetBase:
    method_namespace: Optional[str] = "SearchSnippet"
    using = set([constants.JMAP_URN_MAIL])


@dataclass
class SearchSnippetGet(SearchSnippetBase, Get):
    ids: Optional[ListOrRef[str]] = field(
        metadata=config(field_name="emailIds"), default=None
    )
    filter: Optional[TypeOrRef[EmailQueryFilter]] = None


@dataclass
class SearchSnippetGetResponse(SearchSnippetBase, GetResponseWithoutState):
    data: List[SearchSnippet] = field(metadata=config(field_name="list"))
