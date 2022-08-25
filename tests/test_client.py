import json
from typing import List

import pytest
import requests
import responses

from jmapc import Client
from jmapc.auth import BearerAuth
from jmapc.methods import (
    CoreEcho,
    CoreEchoResponse,
    Invocation,
    InvocationResponseOrError,
    MailboxGet,
    MailboxGetResponse,
    Request,
)
from jmapc.ref import Ref, ResultReference
from jmapc.session import Session, SessionPrimaryAccount

from .utils import expect_jmap_call

echo_test_data = dict(
    who="Ness", goods=["Mr. Saturn coin", "Hall of Fame Bat"]
)


@pytest.mark.parametrize(
    "test_client",
    (
        Client.create_with_api_token(
            "jmap-example.localhost", api_token="ness__pk_fire"
        ),
        Client.create_with_password(
            "jmap-example.localhost", user="ness", password="pk_fire"
        ),
        Client("jmap-example.localhost", auth=("ness", "pk_fire")),
        Client(
            "jmap-example.localhost",
            auth=requests.auth.HTTPBasicAuth(
                username="ness", password="pk_fire"
            ),
        ),
        Client("jmap-example.localhost", auth=BearerAuth("ness__pk_fire")),
    ),
)
def test_jmap_session(
    test_client: Client, http_responses: responses.RequestsMock
) -> None:
    assert test_client.jmap_session == Session(
        username="ness@onett.example.net",
        api_url="https://jmap-api.localhost/api",
        event_source_url=(
            "https://jmap-api.localhost/events/{types}/{closeafter}/{ping}"
        ),
        primary_accounts=SessionPrimaryAccount(
            core="u1138",
            mail="u1138",
            submission="u1138",
        ),
    )


def test_jmap_session_no_account(
    http_responses_base: responses.RequestsMock,
) -> None:
    http_responses_base.add(
        method=responses.GET,
        url="https://jmap-example.localhost/.well-known/jmap",
        body=json.dumps(
            {
                "apiUrl": "https://jmap-api.localhost/api",
                "eventSourceUrl": (
                    "https://jmap-api.localhost/events/"
                    "{types}/{closeafter}/{ping}"
                ),
                "username": "ness@onett.example.net",
                "primary_accounts": {},
            },
        ),
    )
    client = Client.create_with_api_token(
        "jmap-example.localhost", api_token="ness__pk_fire"
    )
    with pytest.raises(Exception) as e:
        client.account_id
    assert str(e.value) == "No primary account ID found"


@pytest.mark.parametrize(
    "method_params",
    [
        [CoreEcho(data=echo_test_data), MailboxGet(ids=Ref("/example"))],
        [
            Invocation(method=CoreEcho(data=echo_test_data), id="0.Core/echo"),
            Invocation(
                method=MailboxGet(ids=Ref(path="/example")), id="1.Mailbox/get"
            ),
        ],
        [
            Invocation(method=CoreEcho(data=echo_test_data), id="0.Core/echo"),
            MailboxGet(ids=Ref("/example", method="0.Core/echo")),
        ],
        [
            CoreEcho(data=echo_test_data),
            MailboxGet(
                ids=ResultReference(
                    path="/example", result_of="0.Core/echo", name="Core/echo"
                )
            ),
        ],
    ],
    ids=[
        "methods_only",
        "invocations_only",
        "method_and_invocation",
        "methods_with_manual_reference",
    ],
)
def test_client_request(
    client: Client,
    http_responses: responses.RequestsMock,
    method_params: List[Request],
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "0.Core/echo",
            ],
            [
                "Mailbox/get",
                {
                    "accountId": "u1138",
                    "#ids": {
                        "name": "Core/echo",
                        "path": "/example",
                        "resultOf": "0.Core/echo",
                    },
                },
                "1.Mailbox/get",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "0.Core/echo",
            ],
            [
                "Mailbox/get",
                {
                    "accountId": "u1138",
                    "list": [],
                    "not_found": [],
                    "state": "1000",
                },
                "1.Mailbox/get",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(method_params) == [
        InvocationResponseOrError(
            response=CoreEchoResponse(data=echo_test_data), id="0.Core/echo"
        ),
        InvocationResponseOrError(
            response=MailboxGetResponse(
                account_id="u1138",
                not_found=[],
                data=[],
                state="1000",
            ),
            id="1.Mailbox/get",
        ),
    ]


@pytest.mark.parametrize("raise_errors", [True, False])
def test_client_request_single(
    client: Client, http_responses: responses.RequestsMock, raise_errors: bool
) -> None:
    method_params = CoreEcho(data=echo_test_data)
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    expected_response = CoreEchoResponse(data=echo_test_data)
    if raise_errors:
        assert (
            client.request(method_params, raise_errors=True)
            == expected_response
        )
    else:
        assert (
            client.request(method_params, raise_errors=False)
            == expected_response
        )


def test_client_request_single_with_multiple_responses(
    client: Client,
    http_responses: responses.RequestsMock,
) -> None:
    method_params = CoreEcho(data=echo_test_data)
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(method_params) == [
        CoreEchoResponse(data=echo_test_data),
        CoreEchoResponse(data=echo_test_data),
    ]


def test_client_request_single_with_multiple_responses_error(
    client: Client,
    http_responses: responses.RequestsMock,
) -> None:
    method_params = CoreEcho(data=echo_test_data)
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    with pytest.raises(RuntimeError):
        client.request(method_params, single_response=True)


def test_client_invalid_single_response_argument(client: Client) -> None:
    with pytest.raises(ValueError):
        client.request(
            [CoreEcho(data=echo_test_data), MailboxGet(ids=[])],
            single_response=True,
        )  # type: ignore


def test_error_unauthorized(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    http_responses.add(
        method=responses.POST,
        url="https://jmap-api.localhost/api",
        status=401,
    )
    with pytest.raises(requests.exceptions.HTTPError) as e:
        client.request(CoreEcho(data=echo_test_data))
    assert e.value.response.status_code == 401
