import json
from typing import Any

import requests

from .config import Config


class JMAP(object):
    def __init__(self) -> None:
        self._config = Config()
        self._session = None

    @property
    def session(self) -> Any:
        if not self._session:
            r = requests.get(
                f"https://{self._config.hostname}/.well-known/jmap",
                auth=(self._config.username, self._config.password),
            )
            r.raise_for_status()
            self._session = r.json()
        return self._session

    @property
    def api_url(self) -> str:
        return self.session["apiUrl"]

    @property
    def account_id(self) -> str:
        return self.session["primaryAccounts"]["urn:ietf:params:jmap:mail"]

    def api_call(self, call: Any) -> Any:
        r = requests.post(
            self.api_url,
            auth=(self._config.username, self._config.password),
            headers={"Content-Type": "application/json"},
            data=json.dumps(call),
        )
        r.raise_for_status()
        return r.json()
