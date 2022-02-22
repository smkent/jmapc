from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional

import requests

from . import constants
from .config import Config
from .types import JMAPCall, JMAPSession


class JMAP(object):
    @dataclass
    class JMAPQueuedCalls:
        using: set[str] = field(
            default_factory=lambda: set([constants.JMAP_URN_CORE])
        )
        calls: list[tuple[str, JMAPCall]] = field(default_factory=list)

        def add(self, call: JMAPCall) -> None:
            self.using |= call.using
            self.calls.append((str(len(self.calls)), call))

        def reset(self) -> None:
            self.using = set([constants.JMAP_URN_CORE])
            self.calls = list()

    def __init__(self) -> None:
        self._config = Config()
        self._session: Optional[JMAPSession] = None
        self._queued = self.JMAPQueuedCalls()

    @property
    def session(self) -> JMAPSession:
        if not self._session:
            r = requests.get(
                f"https://{self._config.hostname}/.well-known/jmap",
                auth=(self._config.username, self._config.password),
            )
            r.raise_for_status()
            self._session = JMAPSession.from_dict(r.json())
        return self._session

    @property
    def api_url(self) -> str:
        return self.session.api_url

    @property
    def account_id(self) -> str:
        return self.session.primary_accounts.mail

    def queue_call(self, call: JMAPCall) -> None:
        self._queued.add(call)

    def exec_calls(self) -> Any:
        return self.api_call(
            {
                "using": list(self._queued.using),
                "methodCalls": [
                    [call[1].name, call[1].to_dict(), call[0]]
                    for call in self._queued.calls
                ],
            },
        )

    def api_call(self, call: Any) -> Any:
        r = requests.post(
            self.session.api_url,
            auth=(self._config.username, self._config.password),
            headers={"Content-Type": "application/json"},
            data=json.dumps(call),
        )
        r.raise_for_status()
        return r.json()
