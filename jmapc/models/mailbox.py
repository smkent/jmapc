from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

from dataclasses_json import config

from ..serializer import Model, null_omitted_field
from .models import Operator, StrOrRef


@dataclass
class Mailbox(Model):
    id: Optional[str] = null_omitted_field(metadata=config(field_name="id"))
    name: Optional[str] = null_omitted_field()
    sort_order: Optional[int] = 0
    total_emails: Optional[int] = null_omitted_field()
    unread_emails: Optional[int] = null_omitted_field()
    total_threads: Optional[int] = null_omitted_field()
    unread_threads: Optional[int] = null_omitted_field()
    is_subscribed: Optional[bool] = False
    role: Optional[str] = null_omitted_field()
    parent_id: Optional[str] = null_omitted_field(
        metadata=config(field_name="parentId"),
    )


@dataclass
class MailboxQueryFilterCondition(Model):
    name: Optional[StrOrRef] = null_omitted_field()
    role: Optional[StrOrRef] = null_omitted_field()
    parent_id: Optional[StrOrRef] = null_omitted_field()
    has_any_role: Optional[bool] = null_omitted_field()
    is_subscribed: Optional[bool] = null_omitted_field()


@dataclass
class MailboxQueryFilterOperator(Model):
    operator: Operator
    conditions: List[MailboxQueryFilter]


MailboxQueryFilter = Union[
    MailboxQueryFilterCondition, MailboxQueryFilterOperator
]
