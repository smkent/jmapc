from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple, Type, Union, cast

import requests

from . import constants, errors
from .logging import log
from .methods import CustomResponse, Method, Response
from .session import Session

MethodList = List[Tuple[str, Method]]
MethodResponseOrError = Union[errors.Error, Response]
MethodResponseList = List[Tuple[str, MethodResponseOrError]]
MethodCallResponseOrList = Union[
    MethodResponseOrError, List[MethodResponseOrError]
]


class Client:
    def __init__(self, host: str, user: str, password: str) -> None:
        self._host: str = host
        self._user: str = user
        self._password: str = password
        self._jmap_session: Optional[Session] = None

    @property
    def jmap_session(self) -> Session:
        if not self._jmap_session:
            r = requests.get(
                f"https://{self._host}/.well-known/jmap",
                auth=(self._user, self._password),
            )
            r.raise_for_status()
            self._jmap_session = Session.from_dict(r.json())
        return self._jmap_session

    @property
    def account_id(self) -> str:
        return self.jmap_session.primary_accounts.mail

    def method_call(
        self, method: Method, flatten_single_response: bool = True
    ) -> MethodCallResponseOrList:
        using = list(set([constants.JMAP_URN_CORE]).union(method.using))
        results = self._api_request(
            {
                "using": sorted(using),
                "methodCalls": [
                    [
                        method.name,
                        method.to_dict(account_id=self.account_id),
                        "uno",
                    ]
                ],
            },
        )
        # One method call may result in multiple responses for that call.
        # If there is a single response, return the response object.
        # Otherwise, return the list of responses.
        if len(results) == 1:
            return results[0][1]
        return [result[1] for result in results]

    def method_calls(
        self, calls: Union[list[Method], MethodList]
    ) -> MethodResponseList:
        if isinstance(calls[0], Method):
            just_calls = cast(List[Method], calls)
            calls = [(str(i), method) for i, method in enumerate(just_calls)]
        calls = cast(MethodList, calls)
        using = list(
            set([constants.JMAP_URN_CORE]).union(*[c[1].using for c in calls])
        )
        return self._api_request(
            {
                "using": sorted(using),
                "methodCalls": [
                    [
                        c[1].name,
                        c[1].to_dict(account_id=self.account_id),
                        c[0],
                    ]
                    for c in calls
                ],
            },
        )

    def _api_request(self, request: Dict[str, Any]) -> MethodResponseList:
        log.debug(f"Sending JMAP request {json.dumps(request)}")
        r = requests.post(
            self.jmap_session.api_url,
            auth=(self._user, self._password),
            headers={"Content-Type": "application/json"},
            data=json.dumps(request),
        )
        r.raise_for_status()
        log.debug(f"Received JMAP response {r.text}")
        return self._parse_responses(r.json())

    def _response_type(self, method_name: str) -> Type[MethodResponseOrError]:
        if method_name == "error":
            return errors.Error
        if method_name in Response.response_types:
            return Response.response_types[method_name]
        return CustomResponse

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
                    self._response_type(name).from_dict(response),
                )
            )
        return responses
