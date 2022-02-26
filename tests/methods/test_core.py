import json

import responses

from jmapc import Client
from jmapc.methods import CoreEcho, CoreEchoResponse


def test_core_echo(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    http_responses.add(
        method=responses.POST,
        url="https://jmap-api.localhost/api",
        body=json.dumps(
            {
                "methodResponses": [
                    [
                        "Core/echo",
                        {
                            "param1": "yes",
                            "another_param": "ok",
                        },
                        "echo_base",
                    ],
                ],
            },
        ),
    )

    test_data = dict(param1="yes", another_param="ok")
    echo = CoreEcho(data=test_data)
    assert echo.to_dict() == test_data
    resp = client.call_method(echo)
    assert resp == CoreEchoResponse(data=test_data)
