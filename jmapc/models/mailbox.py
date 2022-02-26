from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

from dataclasses_json import config

from ..serializer import Model
from .models import Operator, StrOrRef


@dataclass
class Mailbox(Model):
    id: str = field(metadata=config(field_name="Id"))
    name: str
    sort_order: int
    total_emails: int
    unread_emails: int
    total_threads: int
    unread_threads: int
    is_subscribed: bool
    role: Optional[str] = None
    parent_id: Optional[str] = field(
        metadata=config(field_name="parentId"), default=None
    )


@dataclass
class MailboxQueryFilterCondition(Model):
    name: Optional[StrOrRef] = None
    role: Optional[StrOrRef] = None
    parent_id: Optional[StrOrRef] = None


@dataclass
class MailboxQueryFilterOperator(Model):
    operator: Operator
    conditions: List[MailboxQueryFilter]


MailboxQueryFilter = Union[
    MailboxQueryFilterCondition, MailboxQueryFilterOperator
]
