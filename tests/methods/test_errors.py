from typing import Any, Dict

import pytest
import responses

from jmapc import Client, ClientError, Error, errors
from jmapc.methods import CoreEcho, InvocationResponseOrError

from ..utils import expect_jmap_call


@pytest.mark.parametrize("raise_errors", [True, False])
@pytest.mark.parametrize(
    ["method_response", "expected_error"],
    [
        (
            {
                "type": "accountNotFound",
            },
            errors.AccountNotFound(),
        ),
        (
            {
                "type": "accountNotSupportedByMethod",
            },
            errors.AccountNotSupportedByMethod(),
        ),
        (
            {
                "type": "accountReadOnly",
            },
            errors.AccountReadOnly(),
        ),
        (
            {
                "type": "invalidArguments",
                "arguments": ["ids"],
            },
            errors.InvalidArguments(arguments=["ids"]),
        ),
        (
            {
                "type": "invalidResultReference",
            },
            errors.InvalidResultReference(),
        ),
        (
            {
                "type": "forbidden",
            },
            errors.Forbidden(),
        ),
        (
            {
                "type": "serverFail",
                "description": "Something went wrong",
            },
            errors.ServerFail(description="Something went wrong"),
        ),
        (
            {
                "type": "serverPartialFail",
            },
            errors.ServerPartialFail(),
        ),
        (
            {
                "type": "serverUnavailable",
            },
            errors.ServerUnavailable(),
        ),
        (
            {
                "type": "unknownMethod",
            },
            errors.UnknownMethod(),
        ),
        (
            {
                "type": "unsupportedUnitTestErrorType",
                "extraField": "This is an unknown error type",
            },
            errors.Error(type="unsupportedUnitTestErrorType"),
        ),
    ],
)
def test_method_error(
    client: Client,
    http_responses: responses.RequestsMock,
    method_response: Dict[str, Any],
    expected_error: Error,
    raise_errors: bool,
) -> None:
    test_data = dict(param1="yes", another_param="ok")
    expected_request = {
        "methodCalls": [
            ["Core/echo", test_data, "single.Core/echo"],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            ["error", method_response, "single.Core/echo"],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    if raise_errors:
        with pytest.raises(ClientError) as e:
            client.request(CoreEcho(data=test_data), raise_errors=True)
        assert str(e.value) == "Errors found in method responses"
        assert e.value.result == [
            InvocationResponseOrError(
                id="single.Core/echo", response=expected_error
            )
        ]
    else:
        resp = client.request(CoreEcho(data=test_data), raise_errors=False)
        assert resp == expected_error
