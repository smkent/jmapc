from typing import Any, Optional

class SSEClient:
    def __init__(
        self,
        url: str,
        last_id: Optional[str] = None,
        retry: int = 3000,
        session: Optional[Any] = None,
        chunk_size: int = 1024,
        **kwargs: Any
    ):
        pass

    def __iter__(self) -> SSEClient:
        pass

    def __next__(self) -> "Event":
        pass

class Event:
    def __init__(
        self,
        data: str = "",
        event: str = "message",
        id: Optional[str] = None,
        retry: Optional[str] = None,
    ):
        self.data: str
        self.event: str
        self.id: str
        self.retry: str
