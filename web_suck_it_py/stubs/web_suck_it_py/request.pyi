from dataclasses import dataclass
from typing import Any, Dict, Union
from uuid import UUID

@dataclass
class WebSuckItRequest:
    def asdict(self) -> Dict[str, Any]: ...

@dataclass
class GetChannelRequest(WebSuckItRequest):
    channel_name: str
    def __init__(self, channel_name) -> None: ...

@dataclass
class GetOrCreateChannelRequest(GetChannelRequest):
    def __init__(self, channel_name) -> None: ...

@dataclass
class CreateChannelRequest(WebSuckItRequest):
    channel: str
    max_connections: Union[int, None] = ...
    def __init__(self, channel, max_connections) -> None: ...

@dataclass
class DeleteChannelRequest(WebSuckItRequest):
    channel_id: UUID
    def __init__(self, channel_id) -> None: ...

@dataclass
class UpdateChannelRequest(DeleteChannelRequest):
    regenerate_pass_key: bool
    channel: Union[str, None] = ...
    max_connections: Union[int, None] = ...
    def __init__(
        self, channel_id, regenerate_pass_key, channel, max_connections
    ) -> None: ...

@dataclass
class GetChannelListRequest(WebSuckItRequest):
    page: int
    per_page: int
    search_key: Union[str, None] = ...
    def __init__(self, page, per_page, search_key) -> None: ...
