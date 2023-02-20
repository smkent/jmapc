from __future__ import annotations

import functools
import json
import mimetypes
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
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
    Request,
    Response,
    ResponseOrError,
)
from .models import Blob, EmailBodyPart, Event
from .session import Session

RequestsAuth = Union[requests.auth.AuthBase, Tuple[str, str]]
ClientType = TypeVar("ClientType", bound="Client")


@dataclass
class EventSourceConfig:
    types: str = "*"
    closeafter: Literal["state", "no"] = "no"
    ping: int = 0


class Client:
    @classmethod
    def create_with_api_token(
        cls: Type[ClientType],
        host: str,
        api_token: str,
        *args: Any,
        **kwargs: Any,
    ) -> ClientType:
        kwargs["auth"] = BearerAuth(api_token)
        return cls(host, *args, **kwargs)

    @classmethod
    def create_with_password(
        cls: Type[ClientType],
        host: str,
        user: str,
        password: str,
        *args: Any,
        **kwargs: Any,
    ) -> ClientType:
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
            if event.event != "state":
                continue
            yield Event.load_from_sseclient_event(event)

    @functools.cached_property
    def requests_session(self) -> requests.Session:
        requests_session = requests.Session()
        requests_session.auth = self._auth
        return requests_session

    @functools.cached_property
    def jmap_session(self) -> Session:
        r = self.requests_session.get(f"https://{self._host}/.well-known/jmap")
        r.raise_for_status()
        return Session.from_dict(r.json())

    @property
    def account_id(self) -> str:
        primary_account_id = (
            self.jmap_session.primary_accounts.core
            or self.jmap_session.primary_accounts.mail
            or self.jmap_session.primary_accounts.submission
        )
        if not primary_account_id:
            raise Exception("No primary account ID found")
        return primary_account_id

    def upload_blob(self, file_name: Union[str, Path]) -> Blob:
        mime_type, mime_encoding = mimetypes.guess_type(file_name)
        upload_url = self.jmap_session.upload_url.format(
            accountId=self.account_id
        )
        with open(file_name, "rb") as f:
            r = self.requests_session.post(
                upload_url,
                stream=True,
                data=f,
                headers={"Content-Type": mime_type},
            )
        r.raise_for_status()
        return Blob.from_dict(r.json())

    def download_attachment(
        self,
        attachment: EmailBodyPart,
        file_name: Optional[Union[str, Path]] = None,
    ) -> Path:
        file_name = file_name or attachment.name
        if not file_name:
            raise Exception("Unable to determine destination file name")
        file_name = Path(file_name)
        blob_url = self.jmap_session.download_url.format(
            accountId=self.account_id,
            blobId=attachment.blob_id,
            name=file_name.name,
            type=attachment.type,
        )
        r = self.requests_session.get(blob_url, stream=True)
        r.raise_for_status()
        with open(file_name, "wb") as f:
            f.write(r.raw.data)
        return file_name

    @overload
    def request(
        self,
        calls: Method,
        raise_errors: Literal[False] = False,
        single_response: Literal[True] = True,
    ) -> ResponseOrError:
        ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Method,
        raise_errors: Literal[False] = False,
        single_response: Literal[False] = False,
    ) -> Union[Sequence[ResponseOrError], ResponseOrError]:
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
    ) -> Union[Sequence[Response], Response]:
        ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Sequence[Request],
        raise_errors: Literal[False] = False,
    ) -> Sequence[InvocationResponse]:
        ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Sequence[Request],
        raise_errors: Literal[True],
    ) -> Sequence[InvocationResponse]:
        ...  # pragma: no cover

    def request(
        self,
        calls: Union[Sequence[Request], Sequence[Method], Method],
        raise_errors: bool = False,
        single_response: bool = False,
    ) -> Union[
        Sequence[InvocationResponseOrError],
        Sequence[InvocationResponse],
        Union[Sequence[ResponseOrError], ResponseOrError],
        Union[Sequence[Response], Response],
    ]:
        if isinstance(calls, list) and single_response:
            raise ValueError(
                "single_response cannot be used with "
                "multiple JMAP request methods"
            )

        calls_list = calls if isinstance(calls, Sequence) else [calls]
        method_calls: List[Invocation] = []
        # Create Invocations for Methods
        for i, c in enumerate(calls_list):
            if isinstance(c, Invocation):
                method_calls.append(c)
                continue
            method_call_id = (
                f"{i}.{c.jmap_method_name}"
                if len(calls_list) > 1
                else f"single.{c.jmap_method_name}"
            )
            method_calls.append(Invocation(id=method_call_id, method=c))
        # Collect set of JMAP URNs used by all methods in this request
        using = set([constants.JMAP_URN_CORE]).union(
            *[c.method.using for c in method_calls]
        )
        # Validate all requested JMAP URNs are supported by the server
        unsupported_urns = using - self.jmap_session.capabilities.urns
        if unsupported_urns:
            log.warning(
                "URNs in request are not in server capabilities: "
                f"{', '.join(sorted(unsupported_urns))}"
            )
        # Execute request
        result: Union[
            Sequence[InvocationResponseOrError], Sequence[InvocationResponse]
        ] = self._api_request(
            {
                "using": sorted(list(using)),
                "methodCalls": [
                    [
                        c.method.jmap_method_name,
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
                        f"call {method_calls[0].method.jmap_method_name}"
                    )
                return [r.response for r in result]
            return result[0].response
        return result

    def _api_request(
        self, request: Dict[str, Any]
    ) -> Sequence[InvocationResponseOrError]:
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
    ) -> Sequence[InvocationResponseOrError]:
        method_responses = cast(
            Sequence[Tuple[str, Dict[str, Any], str]],
            data.get("methodResponses", []),
        )

        return [
            InvocationResponseOrError(
                id=method_id,
                response=self._response_type(name).from_dict(response),
            )
            for name, response, method_id in method_responses
        ]

    def _response_type(self, method_name: str) -> Type[ResponseOrError]:
        if method_name == "error":
            return errors.Error
        if method_name in Response.response_types:
            return Response.response_types[method_name]
        return CustomResponse
