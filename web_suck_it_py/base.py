import base64
import json
from dataclasses import dataclass
from typing import Any, Dict, TypedDict, Union
from uuid import UUID

import requests
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from web_suck_it_py.constants import HTTPMethod
from web_suck_it_py.error import InitializationError
from web_suck_it_py.versioned_types import NotRequired, Unpack


class GetChannelURLArgs(TypedDict):
    channel_name: str
    channel_pass_key: str
    replay_self: NotRequired[bool]


@dataclass
class Base:
    """Handler for making calls to websuckit platform"""

    user_id: UUID
    access_key: Union[str, None] = None
    public_key: Union[str, None] = None
    base_url: str = "https://backend.websuckit.com/api"
    wss_url: str = "wss://backend.websuckit.com"

    def __generate_channel_path(self, **kwargs: Unpack[GetChannelURLArgs]) -> str:
        channel_name = kwargs.get("channel_name")
        channel_pass_key = kwargs.get("channel_pass_key")
        replay_self = ""
        if kwargs.get("replay_self"):
            replay_self = f"""&replay_self={json.dumps(kwargs.get("replay_self"))}"""
        encoded_token = f"user_id={self.user_id}&channel={channel_name}&channel_pass_key={channel_pass_key}{replay_self}"
        key = RSA.importKey(str(self.public_key))
        cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
        encrypted_token = (
            base64.urlsafe_b64encode(cipher.encrypt(encoded_token.encode()))
            .decode()
            .replace("=", "")
        )
        return f"{self.wss_url}/{self.user_id}/{channel_name}?encrypted_token={encrypted_token}{replay_self}"

    def request(
        self,
        endpoint: str,
        method: HTTPMethod,
        payload: Union[Dict[str, Any], None] = None,
        params: Union[Dict[str, Any], None] = None,
    ) -> requests.Response:
        if self.access_key is None:
            raise InitializationError("access_key")
        headers = {
            "x-user-id": str(self.user_id),
            "x-access-key": self.access_key,
        }
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            url=url,
            method=method,
            headers=headers,
            json=payload,
            params=params,
        )
        response.raise_for_status()
        return response

    def get_connection_url(self, **kwargs: Unpack[GetChannelURLArgs]) -> str:
        if self.public_key is None:
            raise InitializationError("public_key")
        return self.__generate_channel_path(**kwargs)
