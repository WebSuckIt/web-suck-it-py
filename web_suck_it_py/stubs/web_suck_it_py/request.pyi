from typing import Any
from uuid import UUID

class WebSuckItRequest:
    def asdict(self) -> dict[str, Any]: ...

class GetChannelRequest(WebSuckItRequest):
    channel_name: str
    def __init__(self, channel_name) -> None: ...

class GetOrCreateChannelRequest(GetChannelRequest):
    def __init__(self, channel_name) -> None: ...

class CreateChannelRequest(WebSuckItRequest):
    channel: str
    max_connections: int | None
    def __init__(self, channel, max_connections) -> None: ...

class DeleteChannelRequest(WebSuckItRequest):
    channel_id: UUID
    def __init__(self, channel_id) -> None: ...

class UpdateChannelRequest(DeleteChannelRequest):
    regenerate_pass_key: bool
    channel: str | None
    max_connections: int | None
    def __init__(
        self, channel_id, regenerate_pass_key, channel, max_connections
    ) -> None: ...

class GetChannelListRequest(WebSuckItRequest):
    page: int
    per_page: int
    search_key: str | None
    def __init__(self, page, per_page, search_key) -> None: ...
