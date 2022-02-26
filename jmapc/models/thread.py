from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..serializer import Model


@dataclass
class Thread(Model):
    def __len__(self) -> int:
        return len(self.email_ids)

    id: str
    email_ids: List[str]


@dataclass
class ThreadEmail(Model):
    id: str
    mailbox_ids: List[str]
    is_unread: bool
    is_flagged: bool
