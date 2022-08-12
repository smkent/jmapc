import responses

from jmapc import Client, constants
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
                "single.Custom/method",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
    }
    response = {
        "methodResponses": [
            [
                "Custom/method",
                test_data,
                "single.Custom/method",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    method = CustomMethod(data=test_data)
    method.name = "Custom/method"
    method.using = set([constants.JMAP_URN_MAIL])
    assert method.to_dict() == test_data
    resp = client.request(method)
    assert resp == CustomResponse(account_id="u1138", data=test_data)
