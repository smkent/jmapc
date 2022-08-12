import pytest
import requests
import responses

from jmapc import Client
from jmapc.auth import BearerAuth
from jmapc.client import (
    MethodCallResponse,
    MethodCallResponseOrList,
    MethodList,
)
from jmapc.methods import (
    CoreEcho,
    CoreEchoResponse,
    MailboxGet,
    MailboxGetResponse,
)
from jmapc.ref import Ref
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


@pytest.mark.parametrize(
    ["flatten_single_response", "expected_response"],
    [
        (True, CoreEchoResponse(data=echo_test_data)),
        (False, [CoreEchoResponse(data=echo_test_data)]),
    ],
)
def test_method_call(
    client: Client,
    http_responses: responses.RequestsMock,
    flatten_single_response: bool,
    expected_response: MethodCallResponseOrList,
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "uno",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "uno",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
        CoreEcho(data=echo_test_data)
    ) == CoreEchoResponse(data=echo_test_data)


@pytest.mark.parametrize(
    "method_params",
    [
        [CoreEcho(data=echo_test_data), CoreEcho(data=echo_test_data)],
        [
            ("0", CoreEcho(data=echo_test_data)),
            ("1", CoreEcho(data=echo_test_data)),
        ],
    ],
    ids=["methods_only", "custom_ids"],
)
def test_method_calls(
    client: Client,
    http_responses: responses.RequestsMock,
    method_params: MethodList,
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "0",
            ],
            [
                "Core/echo",
                echo_test_data,
                "1",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "0",
            ],
            [
                "Core/echo",
                echo_test_data,
                "1",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    expected_response = CoreEchoResponse(data=echo_test_data)
    assert client.method_calls(method_params) == [
        ("0", expected_response),
        ("1", expected_response),
    ]


@pytest.mark.parametrize(
    "method_params",
    [
        [CoreEcho(data=echo_test_data), MailboxGet(ids=Ref(path="/nope"))],
    ],
    ids=["methods_only"],
)
def test_method_calls_new(
    client: Client,
    http_responses: responses.RequestsMock,
    method_params: MethodList,
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "0",
            ],
            [
                "Mailbox/get",
                {
                    "accountId": "u1138",
                    "#ids": {
                        "name": "Core/echo",
                        "path": "/nope",
                        "resultOf": "0",
                    },
                },
                "1",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "0",
            ],
            [
                "Mailbox/get",
                {
                    "accountId": "u1138",
                    "list": [],
                    "not_found": [],
                    "state": "1000",
                },
                "1",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_calls_new(method_params) == [
        MethodCallResponse(
            response=CoreEchoResponse(data=echo_test_data), id="0"
        ),
        MethodCallResponse(
            response=MailboxGetResponse(
                account_id="u1138",
                not_found=[],
                data=[],
                state="1000",
            ),
            id="1",
        ),
    ]


def test_error_unauthorized(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    http_responses.add(
        method=responses.POST,
        url="https://jmap-api.localhost/api",
        status=401,
    )
    with pytest.raises(requests.exceptions.HTTPError) as e:
        client.method_call(CoreEcho(data=echo_test_data))
    assert e.value.response.status_code == 401
