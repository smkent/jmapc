from typing import Any

class SSEClient:
    def __init__(
        self,
        url: str,
        last_id: str | None = None,
        retry: int = 3000,
        session: Any | None = None,
        chunk_size: int = 1024,
        **kwargs: Any,
    ) -> None: ...
    def __iter__(self) -> SSEClient: ...
    def __next__(self) -> Event: ...

class Event:
    def __init__(
        self,
        data: str = "",
        event: str = "message",
        id: str | None = None,  # noqa: A002
        retry: str | None = None,
    ) -> None: ...
