from dataclasses import dataclass
from typing import Optional

from ..serializer import Model


@dataclass
class SearchSnippet(Model):
    email_id: str
    subject: Optional[str] = None
    preview: Optional[str] = None
