import responses

from jmapc import Client
from jmapc.methods import CoreEcho, CoreEchoResponse

from ..utils import expect_jmap_call


def test_core_echo(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    test_data = dict(param1="yes", another_param="ok")
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                test_data,
                "uno",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                test_data,
                "uno",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    echo = CoreEcho(data=test_data)
    assert echo.to_dict() == test_data
    resp = client.call_method(echo)
    assert resp == CoreEchoResponse(data=test_data)
