from dataclasses import dataclass
from typing import Any, Dict, TypedDict, Union
from uuid import UUID

import requests

from web_suck_it_py.constants import HTTPMethod as HTTPMethod
from web_suck_it_py.error import InitializationError as InitializationError
from web_suck_it_py.versioned_types import NotRequired as NotRequired
from web_suck_it_py.versioned_types import Unpack as Unpack

class GetChannelURLArgs(TypedDict):
    channel_name: str
    channel_pass_key: str
    replay_self: NotRequired[bool]

@dataclass
class Base:
    user_id: UUID
    access_key: Union[str, None] = ...
    public_key: Union[str, None] = ...
    base_url: str = "https://backend.websuckit.com/api"
    wss_url: str = "wss://backend.websuckit.com"
    def request(
        self,
        endpoint: str,
        method: HTTPMethod,
        payload: Union[Dict[str, Any], None] = ...,
        params: Union[Dict[str, Any], None] = ...,
    ) -> requests.Response: ...
    def get_connection_url(self, **kwargs: Unpack[GetChannelURLArgs]) -> str: ...
    def __init__(self, user_id, access_key, public_key, base_url, wss_url) -> None: ...
