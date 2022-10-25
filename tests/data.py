from typing import Any, Dict


def make_session_response() -> Dict[str, Any]:
    return {
        "apiUrl": "https://jmap-api.localhost/api",
        "eventSourceUrl": (
            "https://jmap-api.localhost/events/" "{types}/{closeafter}/{ping}"
        ),
        "username": "ness@onett.example.net",
        "capabilities": {
            "urn:ietf:params:jmap:core": {
                "maxSizeUpload": 50_000_000,
                "maxConcurrentUpload": 4,
                "maxSizeRequest": 10_000_000,
                "maxConcurrentRequests": 4,
                "maxCallsInRequest": 16,
                "maxObjectsInGet": 500,
                "maxObjectsInSet": 500,
                "collationAlgorithms": [
                    "i;ascii-numeric",
                    "i;ascii-casemap",
                    "i;octet",
                ],
            },
        },
        "primaryAccounts": {
            "urn:ietf:params:jmap:core": "u1138",
            "urn:ietf:params:jmap:mail": "u1138",
            "urn:ietf:params:jmap:submission": "u1138",
        },
    }
