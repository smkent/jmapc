import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, api_token: str):
        self.api_token = api_token

    def __call__(
        self, request: requests.models.PreparedRequest
    ) -> requests.models.PreparedRequest:
        request.headers["Authorization"] = f"Bearer {self.api_token}"
        return request
