import responses

from jmapc import Client
from jmapc.methods import CustomMethod, CustomResponse

from ..utils import expect_jmap_call


def test_custom_method(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    test_data = dict(
        accountId="u1138",
        custom_value="Spiteful Crow",
        list_value=["ness", "paula", "jeff", "poo"],
    )
    expected_request = {
        "methodCalls": [
            [
                "Custom/method",
                test_data,
                "uno",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Custom/method",
                test_data,
                "uno",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    method = CustomMethod(data=test_data)
    assert method.to_dict() == test_data
    resp = client.method_call(method)
    assert resp == CustomResponse(account_id="u1138", data=test_data)
