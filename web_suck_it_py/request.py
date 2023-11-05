from dataclasses import asdict, dataclass
from typing import Any
from uuid import UUID


@dataclass
class WebSuckItRequest:
    def asdict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GetChannelRequest(WebSuckItRequest):
    channel_name: str


@dataclass
class GetOrCreateChannelRequest(GetChannelRequest):
    pass


@dataclass
class CreateChannelRequest(WebSuckItRequest):
    channel: str
    max_connections: int | None = None


@dataclass
class DeleteChannelRequest(WebSuckItRequest):
    channel_id: UUID  # used as unique identification as channel name might be in the process of getting updated


@dataclass
class UpdateChannelRequest(DeleteChannelRequest):
    regenerate_pass_key: bool
    channel: str | None = None
    max_connections: int | None = None


@dataclass
class GetChannelListRequest(WebSuckItRequest):
    page: int
    per_page: int
    search_key: str | None = None
