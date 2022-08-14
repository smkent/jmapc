from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from dataclasses_json import config

from .. import constants
from ..models import EmailSubmission, EmailSubmissionQueryFilter
from .base import (
    Changes,
    ChangesResponse,
    Get,
    GetResponse,
    Query,
    QueryResponse,
    Set,
    SetResponse,
)


@dataclass
class EmailSubmissionChanges(Changes):
    name = "EmailSubmission/changes"
    using = set([constants.JMAP_URN_SUBMISSION])


@dataclass
class EmailSubmissionChangesResponse(ChangesResponse):
    name = "EmailSubmission/changes"


@dataclass
class EmailSubmissionGet(Get):
    name = "EmailSubmission/get"
    using = set([constants.JMAP_URN_SUBMISSION])


@dataclass
class EmailSubmissionGetResponse(GetResponse):
    name = "EmailSubmission/get"

    data: List[EmailSubmission] = field(metadata=config(field_name="list"))


@dataclass
class EmailSubmissionQuery(Query):
    name = "EmailSubmission/query"
    using = set([constants.JMAP_URN_SUBMISSION])

    filter: Optional[EmailSubmissionQueryFilter] = None


@dataclass
class EmailSubmissionQueryResponse(QueryResponse):
    name = "EmailSubmission/query"


@dataclass
class EmailSubmissionSet(Set):
    name = "EmailSubmission/set"
    using = set([constants.JMAP_URN_SUBMISSION])

    create: Optional[Dict[str, EmailSubmission]] = None
    on_success_update_email: Optional[Dict[str, Any]] = None
    on_success_destroy_email: Optional[List[str]] = None


@dataclass
class EmailSubmissionSetResponse(SetResponse):
    name = "EmailSubmission/set"

    created: Optional[Dict[str, Optional[EmailSubmission]]]
    updated: Optional[Dict[str, Optional[EmailSubmission]]]
