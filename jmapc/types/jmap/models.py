from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Union

from dataclasses_json import config

from ..util import JsonDataClass


@dataclass
class JMAPIdentity(JsonDataClass):
    id: str
    name: str
    email: str
    replyTo: Optional[str]
    bcc: Optional[List[JMAPIdentityBCC]]
    textSignature: Optional[str]
    htmlSignature: Optional[str]
    mayDelete: bool


@dataclass
class JMAPIdentityBCC(JsonDataClass):
    name: Optional[str]
    email: str


@dataclass
class JMAPMailbox(JsonDataClass):
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
class JMAPEmail(JsonDataClass):
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


@dataclass
class JMAPThread(JsonDataClass):
    def __len__(self) -> int:
        return len(self.email_ids)

    id: str
    email_ids: List[str]


@dataclass
class JMAPThreadEmail(JsonDataClass):
    id: str
    mailbox_ids: List[str]
    is_unread: bool
    is_flagged: bool


@dataclass
class JMAPComparator(JsonDataClass):
    property: str
    is_ascending: bool = True
    collation: Optional[str] = None
    anchor: Optional[str] = None
    anchor_offset: int = 0
    limit: Optional[int] = None
    calculate_total: bool = False
    position: int = 0


@dataclass
class JMAPFilterOperator(JsonDataClass):
    operator: Union[Literal["AND"], Literal["OR"], Literal["NOT"]]


JMAPOperatorLiteral = Union[Literal["AND"], Literal["OR"], Literal["NOT"]]
