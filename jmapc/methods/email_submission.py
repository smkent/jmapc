from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .. import constants
from ..models import EmailSubmission
from .base import Changes, ChangesResponse, Set, SetResponse


@dataclass
class EmailSubmissionChanges(Changes):
    name = "EmailSubmission/changes"
    using = set([constants.JMAP_URN_SUBMISSION])


@dataclass
class EmailSubmissionChangesResponse(ChangesResponse):
    name = "EmailSubmission/changes"


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
