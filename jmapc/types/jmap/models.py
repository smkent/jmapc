from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import DataClassJsonMixin, config


@dataclass
class JMAPIdentity(DataClassJsonMixin):
    id: str
    name: str
    email: str
    replyTo: Optional[str]
    bcc: Optional[List[JMAPIdentityBCC]]
    textSignature: Optional[str]
    htmlSignature: Optional[str]
    mayDelete: bool


@dataclass
class JMAPIdentityBCC(DataClassJsonMixin):
    name: Optional[str]
    email: str


@dataclass
class JMAPMailbox(DataClassJsonMixin):
    id: str = field(metadata=config(field_name="Id"))
    name: str
    sort_order: int = field(metadata=config(field_name="sortOrder"))
    total_emails: int = field(metadata=config(field_name="totalEmails"))
    unread_emails: int = field(metadata=config(field_name="unreadEmails"))
    total_threads: int = field(metadata=config(field_name="totalThreads"))
    unread_threads: int = field(metadata=config(field_name="unreadThreads"))
    is_subsribed: bool = field(metadata=config(field_name="isSubscribed"))
    role: Optional[str] = None
    parent_id: Optional[str] = field(
        metadata=config(field_name="parentId"), default=None
    )


@dataclass
class JMAPEmail(DataClassJsonMixin):
    id: str = field(metadata=config(field_name="Id"))
    blob_id: str = field(metadata=config(field_name="blobId"))
    thread_id: str = field(metadata=config(field_name="threadId"))
    mailboxIds: Dict[str, bool] = field(
        metadata=config(field_name="mailboxIds")
    )
    keywords: Dict[str, bool]
    mail_from: List[str] = field(metadata=config(field_name="from"))
    to: List[str]
    subject: str
    size: int
