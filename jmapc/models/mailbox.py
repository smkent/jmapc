from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union

from dataclasses_json import config

from ..serializer import Model
from .models import Operator, StrOrRef


@dataclass
class Mailbox(Model):
    id: Optional[str] = field(metadata=config(field_name="id"), default=None)
    name: Optional[str] = None
    sort_order: Optional[int] = 0
    total_emails: Optional[int] = None
    unread_emails: Optional[int] = None
    total_threads: Optional[int] = None
    unread_threads: Optional[int] = None
    is_subscribed: Optional[bool] = False
    role: Optional[str] = None
    parent_id: Optional[str] = field(
        metadata=config(field_name="parentId"), default=None
    )


@dataclass
class MailboxQueryFilterCondition(Model):
    name: Optional[StrOrRef] = None
    role: Optional[StrOrRef] = None
    parent_id: Optional[StrOrRef] = None
    has_any_role: Optional[bool] = None
    is_subscribed: Optional[bool] = None


@dataclass
class MailboxQueryFilterOperator(Model):
    operator: Operator
    conditions: list[MailboxQueryFilter]


MailboxQueryFilter = Union[
    MailboxQueryFilterCondition, MailboxQueryFilterOperator
]
