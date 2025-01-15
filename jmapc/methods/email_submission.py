from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from dataclasses_json import config

from .. import constants
from ..models import EmailSubmission, EmailSubmissionQueryFilter
from .base import (
    Changes,
    ChangesResponse,
    Get,
    GetResponse,
    Query,
    QueryChanges,
    QueryChangesResponse,
    QueryResponse,
    Set,
    SetResponse,
)


class EmailSubmissionBase:
    method_namespace: Optional[str] = "EmailSubmission"
    using = {constants.JMAP_URN_SUBMISSION}


@dataclass
class EmailSubmissionChanges(EmailSubmissionBase, Changes):
    pass


@dataclass
class EmailSubmissionChangesResponse(EmailSubmissionBase, ChangesResponse):
    pass


@dataclass
class EmailSubmissionGet(EmailSubmissionBase, Get):
    pass


@dataclass
class EmailSubmissionGetResponse(EmailSubmissionBase, GetResponse):
    data: list[EmailSubmission] = field(metadata=config(field_name="list"))


@dataclass
class EmailSubmissionQuery(EmailSubmissionBase, Query):
    filter: Optional[EmailSubmissionQueryFilter] = None


@dataclass
class EmailSubmissionQueryResponse(EmailSubmissionBase, QueryResponse):
    pass


@dataclass
class EmailSubmissionQueryChanges(EmailSubmissionBase, QueryChanges):
    filter: Optional[EmailSubmissionQueryFilter] = None


@dataclass
class EmailSubmissionQueryChangesResponse(
    EmailSubmissionBase, QueryChangesResponse
):
    pass


@dataclass
class EmailSubmissionSet(EmailSubmissionBase, Set):
    create: Optional[dict[str, EmailSubmission]] = None
    on_success_update_email: Optional[dict[str, Any]] = None
    on_success_destroy_email: Optional[list[str]] = None


@dataclass
class EmailSubmissionSetResponse(EmailSubmissionBase, SetResponse):
    created: Optional[dict[str, Optional[EmailSubmission]]]
    updated: Optional[dict[str, Optional[EmailSubmission]]]
