from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple, Type, Union, cast

import requests

from . import constants
from .types import (
    EmailGetResponse,
    EmailQueryResponse,
    IdentityGetResponse,
    JMAPSession,
    MailboxGetResponse,
    MailboxQueryResponse,
    Method,
    Response,
    ThreadGetResponse,
    errors,
)
from .types.methods import MethodList, MethodResponseList


class JMAPClient:
    METHOD_RESPONSES: Dict[str, Type[Union[errors.JMAPError, Response]]] = {
        "Email/get": EmailGetResponse,
        "Email/query": EmailQueryResponse,
        "Identity/get": IdentityGetResponse,
        "Mailbox/get": MailboxGetResponse,
        "Mailbox/query": MailboxQueryResponse,
        "Thread/get": ThreadGetResponse,
        "error": errors.JMAPError,
    }
    METHOD_RESPONSES_TYPE = Tuple[str, Dict[str, Any], str]

    def __init__(self, host: str, user: str, password: str) -> None:
        self._host: str = host
        self._user: str = user
        self._password: str = password
        self._session: Optional[JMAPSession] = None

    @property
    def session(self) -> JMAPSession:
        if not self._session:
            r = requests.get(
                f"https://{self._host}/.well-known/jmap",
                auth=(self._user, self._password),
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

    def call_method(self, call: Method) -> Any:
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

    def call_methods(self, calls: Union[list[Method], MethodList]) -> Any:
        if isinstance(calls[0], Method):
            just_calls = cast(List[Method], calls)
            calls = [(str(i), call) for i, call in enumerate(just_calls)]
        calls = cast(MethodList, calls)
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

    def _parse_responses(self, data: dict[str, Any]) -> MethodResponseList:
        method_responses = cast(
            List[JMAPClient.METHOD_RESPONSES_TYPE],
            data.get("methodResponses", []),
        )
        responses: MethodResponseList = []
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
            auth=(self._user, self._password),
            headers={"Content-Type": "application/json"},
            data=json.dumps(call),
        )
        r.raise_for_status()
        return self._parse_responses(r.json())
