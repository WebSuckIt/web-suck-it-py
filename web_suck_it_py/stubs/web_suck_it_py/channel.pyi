from dataclasses import dataclass
from typing import List

from web_suck_it_py.base import Base as Base
from web_suck_it_py.constants import HTTPMethod as HTTPMethod
from web_suck_it_py.request import CreateChannelRequest as CreateChannelRequest
from web_suck_it_py.request import DeleteChannelRequest as DeleteChannelRequest
from web_suck_it_py.request import GetChannelListRequest as GetChannelListRequest
from web_suck_it_py.request import GetChannelRequest as GetChannelRequest
from web_suck_it_py.request import (
    GetOrCreateChannelRequest as GetOrCreateChannelRequest,
)
from web_suck_it_py.request import UpdateChannelRequest as UpdateChannelRequest
from web_suck_it_py.response import Channel as Channel

RESOURCE_NAME: str

@dataclass
class WebSuckIt(Base):
    def create_channel(self, params: CreateChannelRequest) -> Channel: ...
    def update_channel(self, params: UpdateChannelRequest) -> Channel: ...
    def get_channel(self, params: GetChannelRequest) -> Channel: ...
    def get_or_create_channel(self, params: GetOrCreateChannelRequest) -> Channel: ...
    def get_channels(self, params: GetChannelListRequest) -> List[Channel]: ...
    def delete_channel(self, params=...) -> None: ...
    def __init__(self, user_id, access_key, public_key, base_url, wss_url) -> None: ...
