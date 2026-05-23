from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar

from dataclasses_json import config

from jmapc import constants
from jmapc.models import EmailSubmission, EmailSubmissionQueryFilter

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
    method_namespace: ClassVar[str | None] = "EmailSubmission"
    using: ClassVar[set[str]] = {constants.JMAP_URN_SUBMISSION}


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
    filter: EmailSubmissionQueryFilter | None = None


@dataclass
class EmailSubmissionQueryResponse(EmailSubmissionBase, QueryResponse):
    pass


@dataclass
class EmailSubmissionQueryChanges(EmailSubmissionBase, QueryChanges):
    filter: EmailSubmissionQueryFilter | None = None


@dataclass
class EmailSubmissionQueryChangesResponse(
    EmailSubmissionBase, QueryChangesResponse
):
    pass


@dataclass
class EmailSubmissionSet(EmailSubmissionBase, Set):
    create: dict[str, EmailSubmission] | None = None
    on_success_update_email: dict[str, Any] | None = None
    on_success_destroy_email: list[str] | None = None


@dataclass
class EmailSubmissionSetResponse(EmailSubmissionBase, SetResponse):
    created: dict[str, EmailSubmission | None] | None
    updated: dict[str, EmailSubmission | None] | None
