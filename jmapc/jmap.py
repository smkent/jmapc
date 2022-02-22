from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple, cast

import requests

from . import constants
from .config import Config
from .types.jmap import (
    JMAPIdentityGetResponse,
    JMAPMethod,
    JMAPResponse,
    JMAPSession,
)

JMAPMethodPair = Tuple[str, JMAPMethod]
JMAPMethodResponsePair = Tuple[str, JMAPResponse]


class JMAP(object):
    METHOD_RESPONSES = {
        "Identity/get": JMAPIdentityGetResponse,
    }
    METHOD_RESPONSES_TYPE = Tuple[str, Dict[str, Any], str]

    def __init__(self) -> None:
        self._config = Config()
        self._session: Optional[JMAPSession] = None

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

    def call_method(self, call: JMAPMethod) -> Any:
        using = list(set([constants.JMAP_URN_CORE]).union(call.using))
        result = self._api_call(
            {
                "using": using,
                "methodCalls": [[call.name, call.to_dict(), "uno"]],
            },
        )
        return result[0][1]

    def call_methods(self, calls: list[JMAPMethodPair]) -> Any:
        using = list(
            set([constants.JMAP_URN_CORE]).union(*[c[1].using for c in calls])
        )
        return self._api_call(
            {
                "using": using,
                "methodCalls": [
                    [c[1].name, c[1].to_dict(), c[0]] for c in calls
                ],
            },
        )

    def _parse_responses(
        self, data: dict[str, Any]
    ) -> list[JMAPMethodResponsePair]:
        method_responses = cast(
            List[JMAP.METHOD_RESPONSES_TYPE],
            data.get("methodResponses", []),
        )
        responses: list[JMAPMethodResponsePair] = []
        for name, response, method_id in method_responses:
            responses.append(
                (
                    method_id,
                    self.METHOD_RESPONSES[name].from_dict(response),
                )
            )
        return responses

    def _api_call(self, call: Any) -> Any:
        r = requests.post(
            self.session.api_url,
            auth=(self._config.username, self._config.password),
            headers={"Content-Type": "application/json"},
            data=json.dumps(call),
        )
        r.raise_for_status()
        return self._parse_responses(r.json())
