from dataclasses import dataclass
from typing import Any, Dict, List

from web_suck_it_py.base import Base
from web_suck_it_py.constants import HTTPMethod
from web_suck_it_py.request import (
    CreateChannelRequest,
    DeleteChannelRequest,
    GetChannelListRequest,
    GetChannelRequest,
    GetOrCreateChannelRequest,
    UpdateChannelRequest,
)
from web_suck_it_py.response import Channel

RESOURCE_NAME = "channel"


@dataclass
class WebSuckIt(Base):
    def create_channel(self, params: CreateChannelRequest) -> Channel:
        response = self.request(
            endpoint=f"/{RESOURCE_NAME}/create",
            method=HTTPMethod.POST,
            payload=params.asdict(),
        )
        return Channel(**response.json()["channel"])

    def update_channel(self, params: UpdateChannelRequest) -> Channel:
        params_parsed: Dict[str, Any] = params.asdict()
        channel_id = str(params_parsed.pop("channel_id"))
        response = self.request(
            endpoint=f"/{RESOURCE_NAME}/{channel_id}/update",
            method=HTTPMethod.PUT,
            payload=params_parsed,
        )
        return Channel(**response.json()["channel"])

    def get_channel(self, params: GetChannelRequest) -> Channel:
        response = self.request(
            endpoint=f"/{RESOURCE_NAME}/{params.channel_name}/details",
            method=HTTPMethod.GET,
        )
        return Channel(**response.json())

    def get_or_create_channel(self, params: GetOrCreateChannelRequest) -> Channel:
        response = self.request(
            endpoint=f"/{RESOURCE_NAME}/{params.channel_name}/get-or-create",
            method=HTTPMethod.GET,
        )
        return Channel(**response.json())

    def get_channels(self, params: GetChannelListRequest) -> List[Channel]:
        response = self.request(
            endpoint=f"/{RESOURCE_NAME}/list",
            method=HTTPMethod.GET,
            params=params.asdict(),
        )
        return [Channel(**channel) for channel in response.json()]

    def delete_channel(self, params=DeleteChannelRequest):
        params = params.asdict()
        channel_id = str(params.pop("channel_id"))
        self.request(
            endpoint=f"/{RESOURCE_NAME}/{channel_id}/delete",
            method=HTTPMethod.DELETE,
        )
