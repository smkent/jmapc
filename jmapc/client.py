from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple, Type, Union, cast

import requests

from . import constants
from .config import Config
from .types import (
    JMAPEmailGetResponse,
    JMAPEmailQueryResponse,
    JMAPIdentityGetResponse,
    JMAPMailboxGetResponse,
    JMAPMailboxQueryResponse,
    JMAPMethod,
    JMAPResponse,
    JMAPSession,
    JMAPThreadGetResponse,
    errors,
)

JMAPMethodPair = Tuple[str, JMAPMethod]
JMAPMethodResponsePair = Tuple[str, Union[errors.JMAPError, JMAPResponse]]


class JMAP(object):
    METHOD_RESPONSES: Dict[
        str, Type[Union[errors.JMAPError, JMAPResponse]]
    ] = {
        "Email/get": JMAPEmailGetResponse,
        "Email/query": JMAPEmailQueryResponse,
        "Identity/get": JMAPIdentityGetResponse,
        "Mailbox/get": JMAPMailboxGetResponse,
        "Mailbox/query": JMAPMailboxQueryResponse,
        "Thread/get": JMAPThreadGetResponse,
        "error": errors.JMAPError,
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
        using = list(set([constants.JMAP_URN_CORE]).union(call.using()))
        result = self._api_call(
            {
                "using": using,
                "methodCalls": [
                    [
                        call.name(),
                        call.to_dict(account_id=self.account_id),
                        "uno",
                    ]
                ],
            },
        )
        return result[0][1]

    def call_methods(
        self, calls: Union[list[JMAPMethod], list[JMAPMethodPair]]
    ) -> Any:
        if isinstance(calls[0], JMAPMethod):
            just_calls = cast(List[JMAPMethod], calls)
            calls = [(str(i), call) for i, call in enumerate(just_calls)]
        calls = cast(List[JMAPMethodPair], calls)
        using = list(
            set([constants.JMAP_URN_CORE]).union(
                *[c[1].using() for c in calls]
            )
        )
        return self._api_call(
            {
                "using": using,
                "methodCalls": [
                    [
                        c[1].name(),
                        c[1].to_dict(account_id=self.account_id),
                        c[0],
                    ]
                    for c in calls
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
