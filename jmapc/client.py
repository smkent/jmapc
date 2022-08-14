from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
    overload,
)

import requests
import sseclient

from . import constants, errors
from .auth import BearerAuth
from .logging import log
from .methods import (
    CustomResponse,
    Invocation,
    InvocationResponse,
    InvocationResponseOrError,
    Method,
    Response,
)
from .models import Event
from .session import Session

MethodList = List[Tuple[str, Method]]
MethodResponseOrError = Union[errors.Error, Response]
MethodResponseList = List[Tuple[str, MethodResponseOrError]]
MethodCallResponseOrList = Union[
    MethodResponseOrError, List[MethodResponseOrError]
]
RequestsAuth = Union[requests.auth.AuthBase, Tuple[str, str]]


InvocationOrMethod = Union[Method, Invocation]


@dataclass
class EventSourceConfig:
    types: str = "*"
    closeafter: Literal["state", "no"] = "no"
    ping: int = 0


class Client:
    @classmethod
    def create_with_api_token(
        cls, host: str, api_token: str, *args: Any, **kwargs: Any
    ) -> Client:
        kwargs["auth"] = BearerAuth(api_token)
        return cls(host, *args, **kwargs)

    @classmethod
    def create_with_password(
        cls, host: str, user: str, password: str, *args: Any, **kwargs: Any
    ) -> Client:
        kwargs["auth"] = requests.auth.HTTPBasicAuth(
            username=user, password=password
        )
        return cls(host, *args, **kwargs)

    def __init__(
        self,
        host: str,
        auth: Optional[RequestsAuth] = None,
        last_event_id: Optional[str] = None,
        event_source_config: Optional[EventSourceConfig] = None,
    ) -> None:
        self._host: str = host
        self._auth: Optional[RequestsAuth] = auth
        self._last_event_id: Optional[str] = last_event_id
        self._event_source_config: EventSourceConfig = (
            event_source_config or EventSourceConfig()
        )
        self._jmap_session: Optional[Session] = None
        self._requests_session: Optional[requests.Session] = None
        self._events: Optional[sseclient.SSEClient] = None

    @property
    def events(self) -> Generator[Event, None, None]:
        if not self._events:
            self._events = sseclient.SSEClient(
                self.jmap_session.event_source_url.format(
                    **asdict(self._event_source_config)
                ),
                auth=self.requests_session.auth,
                last_id=self._last_event_id,
            )
        for event in self._events:
            if not event.id or event.event != "state":
                continue
            yield Event.load_from_sseclient_event(event)

    @property
    def requests_session(self) -> requests.Session:
        if not self._requests_session:
            self._requests_session = requests.Session()
            self._requests_session.auth = self._auth
        return self._requests_session

    @property
    def jmap_session(self) -> Session:
        if not self._jmap_session:
            r = self.requests_session.get(
                f"https://{self._host}/.well-known/jmap"
            )
            r.raise_for_status()
            self._jmap_session = Session.from_dict(r.json())
        return self._jmap_session

    @property
    def account_id(self) -> str:
        return self.jmap_session.primary_accounts.mail

    @overload
    def request(
        self,
        calls: Method,
        raise_errors: Literal[False] = False,
        single_response: Literal[True] = True,
    ) -> MethodResponseOrError:
        ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Method,
        raise_errors: Literal[False] = False,
        single_response: Literal[False] = False,
    ) -> Union[List[MethodResponseOrError], MethodResponseOrError]:
        ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Method,
        raise_errors: Literal[True],
        single_response: Literal[True],
    ) -> Response:
        ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Method,
        raise_errors: Literal[True],
        single_response: Literal[False] = False,
    ) -> Union[List[Response], Response]:
        ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: List[InvocationOrMethod],
        raise_errors: Literal[False] = False,
    ) -> List[InvocationResponse]:
        ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: List[InvocationOrMethod],
        raise_errors: Literal[True],
    ) -> List[InvocationResponse]:
        ...  # pragma: no cover

    def request(
        self,
        calls: Union[List[InvocationOrMethod], Method],
        raise_errors: bool = False,
        single_response: bool = False,
    ) -> Union[
        List[InvocationResponseOrError],
        List[InvocationResponse],
        Union[List[MethodResponseOrError], MethodResponseOrError],
        Union[List[Response], Response],
    ]:
        if isinstance(calls, list):
            if single_response:
                raise ValueError(
                    "single_response cannot be used with "
                    "multiple JMAP request methods"
                )

        calls_list = calls if isinstance(calls, list) else [calls]
        method_calls: List[Invocation] = []
        # Create Invocations for Methods
        for i, c in enumerate(calls_list):
            if isinstance(c, Invocation):
                method_calls.append(c)
                continue
            method_call_id = (
                f"{i}.{c.name}" if len(calls_list) > 1 else f"single.{c.name}"
            )
            method_calls.append(Invocation(id=method_call_id, method=c))
        # Collect set of JMAP URNs used by all methods in this request
        using = list(
            set([constants.JMAP_URN_CORE]).union(
                *[c.method.using for c in method_calls]
            )
        )
        # Execute request
        result: Union[
            List[InvocationResponseOrError], List[InvocationResponse]
        ] = self._api_request(
            {
                "using": sorted(using),
                "methodCalls": [
                    [
                        c.method.name,
                        c.method.to_dict(
                            account_id=self.account_id,
                            method_calls_slice=method_calls[:i],
                            encode_json=True,
                        ),
                        c.id,
                    ]
                    for i, c in enumerate(method_calls)
                ],
            },
        )
        if raise_errors:
            if any(isinstance(r.response, errors.Error) for r in result):
                raise RuntimeError("Errors found")
            result = [
                InvocationResponse(
                    id=r.id, response=cast(Response, r.response)
                )
                for r in result
            ]
        if isinstance(calls, Method):
            if len(result) > 1:
                if single_response:
                    raise RuntimeError(
                        f"{len(result)} results received for single method "
                        f"call {method_calls[0].method.name}"
                    )
                return [r.response for r in result]
            return result[0].response
        return result

    def _api_request(
        self, request: Dict[str, Any]
    ) -> List[InvocationResponseOrError]:
        log.debug(f"Sending JMAP request {json.dumps(request)}")
        r = self.requests_session.post(
            self.jmap_session.api_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(request),
        )
        r.raise_for_status()
        log.debug(f"Received JMAP response {r.text}")
        return self._parse_method_responses(r.json())

    def _parse_method_responses(
        self, data: dict[str, Any]
    ) -> List[InvocationResponseOrError]:
        method_responses = cast(
            List[Tuple[str, Dict[str, Any], str]],
            data.get("methodResponses", []),
        )
        return [
            InvocationResponseOrError(
                id=method_id,
                response=self._response_type(name).from_dict(response),
            )
            for name, response, method_id in method_responses
        ]

    def _response_type(self, method_name: str) -> Type[MethodResponseOrError]:
        if method_name == "error":
            return errors.Error
        if method_name in Response.response_types:
            return Response.response_types[method_name]
        return CustomResponse
