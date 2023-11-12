from typing import Optional, Any
from uuid import UUID
from websocket import create_connection
from web_suck_it_py import (
    WebSuckIt,
    GetOrCreateChannelRequest,
    Channel,
)
from .config import Config


class Suckit:
    """
    Class to interact with the WebSuckIt API.
    """

    def __init__(
        self,
        user_id: Optional[UUID] = None,
        access_key: Optional[str] = None,
        public_key: Optional[str] = None,
        channel_name: Optional[str] = None,
        channel_pass_key: Optional[str] = None,
    ) -> None:
        """
        Initialize the class.
        Args:
            user_id (UUID): User ID (default: Config.websuckit_user_id)
            access_key (str): Access key (default: Config.websuckit_api_key)
            public_key (str): Public key (default: Config.websuckit_public_key)
            channel_name (str): Channel name (default: Config.websuckit_channel_name)
            channel_pass_key (str): Channel pass key (default: Config.websuckit_channel_pass_key)
        """
        self.user_id = user_id or Config.websuckit_user_id
        self.__access_key = access_key or Config.websuckit_api_key
        self.__public_key = public_key or Config.websuckit_public_key
        self.channel_name = channel_name or Config.websuckit_channel_name
        self.__channel_pass_key = channel_pass_key or Config.websuckit_channel_pass_key
        self.handler = WebSuckIt(
            user_id=self.user_id,
            access_key=self.__access_key,
            public_key=self.__public_key,
        )

    def get_uri(self, **kwargs) -> str:
        """
        Get the connection URL for a channel.
        Args:
            channel_name (str): Channel name
        Returns:
            str: Connection URL
        """

        channel: Channel = self.handler.get_or_create_channel(
            GetOrCreateChannelRequest(
                channel_name=self.channel_name,
            )
        )  # Get or create the channel if it doesn't exist
        return self.handler.get_connection_url(
            channel_name=channel.name,
            channel_pass_key=channel.pass_key,
            **kwargs,
        )  # Get the connection URL for the channel


def standalone_send(payload: Any, ws_uri: str) -> None:
    """
    Standalone function to send data to a WebSocket server. This function connects to the WebSocket server, sends the data, and closes the connection.
    Returns:
        None
    """
    websocket = create_connection(ws_uri)
    try:
        # Send JSON data to the WebSocket server
        websocket.send(payload)
        print(f"Successfully sent JSON data to {ws_uri}")
    finally:
        # Close the WebSocket connection
        websocket.close()
