from typing import Any, Dict

import pytest
import responses

from jmapc import Client, Error, errors
from jmapc.methods import CoreEcho

from ..utils import expect_jmap_call


@pytest.mark.parametrize(
    ["method_response", "expected_error"],
    [
        (
            {
                "type": "serverFail",
                "description": "Something went wrong",
            },
            errors.ServerFail(
                type="serverFail", description="Something went wrong"
            ),
        ),
        (
            {
                "type": "invalidArguments",
                "arguments": ["ids"],
            },
            errors.InvalidArguments(
                type="invalidArguments", arguments=["ids"]
            ),
        ),
    ],
)
def test_method_error(
    client: Client,
    http_responses: responses.RequestsMock,
    method_response: Dict[str, Any],
    expected_error: Error,
) -> None:
    test_data = dict(param1="yes", another_param="ok")
    expected_request = {
        "methodCalls": [
            ["Core/echo", test_data, "uno"],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            ["error", method_response, "uno"],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    resp = client.method_call(CoreEcho(data=test_data))
    assert resp == expected_error
