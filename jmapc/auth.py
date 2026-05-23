from __future__ import annotations

from typing import TYPE_CHECKING

from requests.auth import AuthBase

if TYPE_CHECKING:
    from requests.models import PreparedRequest


class BearerAuth(AuthBase):
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["Authorization"] = f"Bearer {self.api_token}"
        return r
