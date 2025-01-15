from __future__ import annotations

import functools
import mimetypes
from collections.abc import Generator, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal, Optional, TypeVar, Union, cast, overload

import requests
import sseclient

from . import errors
from .api import APIRequest, APIResponse
from .auth import BearerAuth
from .logging import log
from .methods import (
    InvocationResponse,
    InvocationResponseOrError,
    Method,
    Request,
    Response,
    ResponseOrError,
)
from .models import Blob, EmailBodyPart, Event
from .session import Session

RequestsAuth = Union[requests.auth.AuthBase, tuple[str, str]]
ClientType = TypeVar("ClientType", bound="Client")

REQUEST_TIMEOUT = 30


@dataclass
class EventSourceConfig:
    types: str = "*"
    closeafter: Literal["state", "no"] = "no"
    ping: int = 0


class ClientError(RuntimeError):
    def __init__(
        self,
        *args: Any,
        result: Sequence[Union[InvocationResponse, InvocationResponseOrError]],
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.result = result


class Client:
    @classmethod
    def create_with_api_token(
        cls: type[ClientType],
        host: str,
        api_token: str,
        *args: Any,
        **kwargs: Any,
    ) -> ClientType:
        kwargs["auth"] = BearerAuth(api_token)
        return cls(host, *args, **kwargs)

    @classmethod
    def create_with_password(
        cls: type[ClientType],
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
        r = self.requests_session.get(
            f"https://{self._host}/.well-known/jmap", timeout=REQUEST_TIMEOUT
        )
        r.raise_for_status()
        session = Session.from_dict(r.json())
        log.debug(f"Retrieved JMAP session with state {session.state}")
        return session

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
                timeout=REQUEST_TIMEOUT,
            )
        r.raise_for_status()
        return Blob.from_dict(r.json())

    def download_attachment(
        self,
        attachment: EmailBodyPart,
        file_name: Union[str, Path],
    ) -> None:
        if not file_name:
            raise Exception("Destination file name is required")
        file_name = Path(file_name)
        blob_url = self.jmap_session.download_url.format(
            accountId=self.account_id,
            blobId=attachment.blob_id,
            name=attachment.name,
            type=attachment.type,
        )
        r = self.requests_session.get(
            blob_url, stream=True, timeout=REQUEST_TIMEOUT
        )
        r.raise_for_status()
        with open(file_name, "wb") as f:
            f.write(r.raw.data)

    @overload
    def request(
        self,
        calls: Method,
        raise_errors: Literal[False] = False,
        single_response: Literal[True] = True,
    ) -> ResponseOrError: ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Method,
        raise_errors: Literal[False] = False,
        single_response: Literal[False] = False,
    ) -> Union[
        Sequence[ResponseOrError], ResponseOrError
    ]: ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Method,
        raise_errors: Literal[True],
        single_response: Literal[True],
    ) -> Response: ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Method,
        raise_errors: Literal[True],
        single_response: Literal[False] = False,
    ) -> Union[Sequence[Response], Response]: ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Sequence[Request],
        raise_errors: Literal[False] = False,
    ) -> Sequence[InvocationResponse]: ...  # pragma: no cover

    @overload
    def request(
        self,
        calls: Sequence[Request],
        raise_errors: Literal[True],
    ) -> Sequence[InvocationResponse]: ...  # pragma: no cover

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
        api_request = APIRequest.from_calls(self.account_id, calls)
        # Validate all requested JMAP URNs are supported by the server
        unsupported_urns = (
            api_request.using - self.jmap_session.capabilities.urns
        )
        if unsupported_urns:
            log.warning(
                "URNs in request are not in server capabilities: "
                f"{', '.join(sorted(unsupported_urns))}"
            )
        # Execute request
        result: Union[
            Sequence[InvocationResponseOrError], Sequence[InvocationResponse]
        ] = self._api_request(api_request)
        if raise_errors:
            if any(isinstance(r.response, errors.Error) for r in result):
                raise ClientError(
                    "Errors found in method responses", result=result
                )
            result = [
                InvocationResponse(
                    id=r.id, response=cast(Response, r.response)
                )
                for r in result
            ]
        if isinstance(calls, Method):
            if len(result) > 1:
                if single_response:
                    raise ClientError(
                        f"{len(result)} method responses received for single"
                        f" method call {api_request.method_calls[0][0]}",
                        result=result,
                    )
                return [r.response for r in result]
            return result[0].response
        return result

    def _api_request(
        self, request: APIRequest
    ) -> Sequence[InvocationResponseOrError]:
        raw_request = request.to_json()
        log.debug(f"Sending JMAP request {raw_request}")
        r = self.requests_session.post(
            self.jmap_session.api_url,
            headers={"Content-Type": "application/json"},
            data=raw_request,
            timeout=REQUEST_TIMEOUT,
        )
        r.raise_for_status()
        log.debug(f"Received JMAP response {r.text}")
        api_response = APIResponse.from_dict(r.json())
        if api_response.session_state != self.jmap_session.state:
            log.debug(
                "JMAP response session state"
                f' "{api_response.session_state}" differs from cached state'
                f'"{self.jmap_session.state}", invalidating cached state'
            )
            del self.jmap_session
        return api_response.method_responses
