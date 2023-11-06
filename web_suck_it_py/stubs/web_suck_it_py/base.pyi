from http import HTTPMethod
from typing import Any, NotRequired, TypedDict, Unpack
from uuid import UUID

import requests

from web_suck_it_py.error import InitializationError as InitializationError

class GetChannelURLArgs(TypedDict):
    channel_name: str
    channel_pass_key: str
    replay_self: NotRequired[bool]

class Base:
    user_id: UUID
    access_key: str | None
    public_key: str | None
    base_url: str = "https://backend.websuckit.com/api"
    wss_url: str = "wss://backend.websuckit.com"
    def request(
        self,
        endpoint: str,
        method: HTTPMethod,
        payload: dict[str, Any] | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> requests.Response: ...
    def get_connection_url(self, **kwargs: Unpack[GetChannelURLArgs]) -> str: ...
    def __init__(self, user_id, access_key, public_key, base_url, wss_url) -> None: ...
