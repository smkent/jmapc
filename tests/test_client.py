import json
from typing import Dict, Tuple

import pytest
import requests
import responses

from jmapc import Client
from jmapc.client import MethodList
from jmapc.methods import CoreEcho, CoreEchoResponse
from jmapc.session import Session, SessionPrimaryAccount

echo_test_data = dict(
    who="Ness", goods=["Mr. Saturn coin", "Hall of Fame Bat"]
)


def test_session(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    assert client.session == Session(
        username="ness@onett.example.net",
        api_url="https://jmap-api.localhost/api",
        primary_accounts=SessionPrimaryAccount(
            core="u1138",
            mail="u1138",
            submission="u1138",
        ),
    )


def test_call_method(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    def _response(
        request: requests.PreparedRequest,
    ) -> Tuple[int, Dict[str, str], str]:
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.body or "{}") == {
            "methodCalls": [
                [
                    "Core/echo",
                    echo_test_data,
                    "uno",
                ],
            ],
            "using": ["urn:ietf:params:jmap:core"],
        }
        return (
            200,
            dict(),
            json.dumps(
                {
                    "methodResponses": [
                        [
                            "Core/echo",
                            echo_test_data,
                            "uno",
                        ],
                    ],
                },
            ),
        )

    http_responses.add_callback(
        method=responses.POST,
        url="https://jmap-api.localhost/api",
        callback=_response,
    )
    assert client.call_method(
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
def test_call_methods(
    client: Client,
    http_responses: responses.RequestsMock,
    method_params: MethodList,
) -> None:
    def _response(
        request: requests.PreparedRequest,
    ) -> Tuple[int, Dict[str, str], str]:
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.body or "{}") == {
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
        return (
            200,
            dict(),
            json.dumps(
                {
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
                },
            ),
        )

    http_responses.add_callback(
        method=responses.POST,
        url="https://jmap-api.localhost/api",
        callback=_response,
    )
    expected_response = CoreEchoResponse(data=echo_test_data)
    assert client.call_methods(method_params) == [
        ("0", expected_response),
        ("1", expected_response),
    ]
