import functools
import json
from typing import Any, Callable, Dict, Tuple

import requests
import responses


def assert_request_return_response(
    expected_request: Dict[str, Any],
    response: Dict[str, Any],
) -> Callable[[requests.PreparedRequest], Tuple[int, Dict[str, str], str]]:
    def _response_callback(
        expected_request: Dict[str, Any],
        response: Dict[str, Any],
        request: requests.PreparedRequest,
    ) -> Tuple[int, Dict[str, str], str]:
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.body or "{}") == expected_request
        return (200, dict(), json.dumps(response))

    return functools.partial(_response_callback, expected_request, response)


def expect_jmap_call(
    http_responses: responses.RequestsMock,
    expected_request: Dict[str, Any],
    response: Dict[str, Any],
) -> None:
    http_responses.add_callback(
        method=responses.POST,
        url="https://jmap-api.localhost/api",
        callback=assert_request_return_response(expected_request, response),
    )
