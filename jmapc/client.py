from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple, Type, Union, cast

import requests

from . import constants, errors
from .logging import log
from .methods import (
    CoreEchoResponse,
    EmailGetResponse,
    EmailQueryResponse,
    EmailSetResponse,
    IdentityGetResponse,
    MailboxGetResponse,
    MailboxQueryResponse,
    Method,
    Response,
    ThreadGetResponse,
)
from .session import Session

MethodList = List[Tuple[str, Method]]
MethodResponseList = List[Tuple[str, Union[errors.Error, Response]]]


class Client:
    METHOD_RESPONSES: Dict[str, Type[Union[errors.Error, Response]]] = {
        "Core/echo": CoreEchoResponse,
        "Email/get": EmailGetResponse,
        "Email/set": EmailSetResponse,
        "Email/query": EmailQueryResponse,
        "Identity/get": IdentityGetResponse,
        "Mailbox/get": MailboxGetResponse,
        "Mailbox/query": MailboxQueryResponse,
        "Thread/get": ThreadGetResponse,
        "error": errors.Error,
    }

    def __init__(self, host: str, user: str, password: str) -> None:
        self._host: str = host
        self._user: str = user
        self._password: str = password
        self._session: Optional[Session] = None

    @property
    def session(self) -> Session:
        if not self._session:
            r = requests.get(
                f"https://{self._host}/.well-known/jmap",
                auth=(self._user, self._password),
            )
            r.raise_for_status()
            self._session = Session.from_dict(r.json())
        return self._session

    @property
    def account_id(self) -> str:
        return self.session.primary_accounts.mail

    def method_call(self, method: Method) -> Any:
        using = list(set([constants.JMAP_URN_CORE]).union(method.using()))
        result = self._api_request(
            {
                "using": sorted(using),
                "methodCalls": [
                    [
                        method.name(),
                        method.to_dict(account_id=self.account_id),
                        "uno",
                    ]
                ],
            },
        )
        return result[0][1]

    def method_calls(self, calls: Union[list[Method], MethodList]) -> Any:
        if isinstance(calls[0], Method):
            just_calls = cast(List[Method], calls)
            calls = [(str(i), method) for i, method in enumerate(just_calls)]
        calls = cast(MethodList, calls)
        using = list(
            set([constants.JMAP_URN_CORE]).union(
                *[c[1].using() for c in calls]
            )
        )
        return self._api_request(
            {
                "using": sorted(using),
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

    def _api_request(self, request: Any) -> Any:
        log.debug(f"Sending JMAP request {json.dumps(request)}")
        r = requests.post(
            self.session.api_url,
            auth=(self._user, self._password),
            headers={"Content-Type": "application/json"},
            data=json.dumps(request),
        )
        r.raise_for_status()
        log.debug(f"Received JMAP response {r.text}")
        return self._parse_responses(r.json())

    def _parse_responses(self, data: dict[str, Any]) -> MethodResponseList:
        method_responses = cast(
            List[Tuple[str, Dict[str, Any], str]],
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
