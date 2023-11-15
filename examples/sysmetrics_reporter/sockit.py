from typing import Any, Generator, Optional
from uuid import UUID

from config import Config, logging
from websocket import create_connection

from web_suck_it_py import Channel, GetOrCreateChannelRequest, WebSuckIt


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
    ) -> None:
        """
        Initialize the class.
        Args:
            user_id (UUID): User ID (default: Config.websuckit_user_id)
            access_key (str): Access key (default: Config.websuckit_user_access_key)
            public_key (str): Public key (default: Config.websuckit_public_key)
            channel_name (str): Channel name (default: Config.websuckit_channel_name)
        """
        self.user_id = user_id or Config.websuckit_user_id
        self.__access_key = access_key or Config.websuckit_user_access_key
        self.__public_key = public_key or Config.websuckit_public_key
        channel_name = channel_name or Config.websuckit_channel_name
        self.handler = WebSuckIt(
            user_id=self.user_id,
            access_key=self.__access_key,
            public_key=self.__public_key,
        )
        self._channel: Channel = self.handler.get_or_create_channel(
            GetOrCreateChannelRequest(
                channel_name=channel_name,
            )
        )  # Get or create the channel if it doesn't exist

    @property
    def channel(self) -> Channel:
        """
        Get the channel.
        Returns:
            Channel: Channel
        """
        return self._channel

    @channel.setter
    def channel(self, channel_name: str) -> None:
        """
        Set the channel.
        Args:
            channel_name (Channel): Channel
        """
        self.channel: Channel = self.handler.get_or_create_channel(
            GetOrCreateChannelRequest(
                channel_name=channel_name,
            )
        )  # Get or create the channel if it doesn't exist

    def get_uri(self, **kwargs) -> str:
        """
        Get the connection URL for a channel.
        Args:
            channel_name (str): Channel name
        Returns:
            str: Connection URL
        """
        logging.debug(f"Getting connection URL for {self.channel.name} ...")
        uri = self.handler.get_connection_url(
            channel_name=self.channel.name,
            channel_pass_key=self.channel.pass_key,
            **kwargs,
        )  # Get the connection URL for the channel
        logging.debug(f"Connection URL : {uri}")
        return uri


def standalone_send(payload: Any, ws_uri: str) -> None:
    """
    Standalone function to send data to a WebSocket server. This function connects to the WebSocket server, sends the data, and closes the connection.
    Args:
        payload (Any): Data to send to the WebSocket server
        ws_uri (str): WebSocket URI
    Returns:
        None
    """
    websocket = create_connection(ws_uri)
    try:
        # Send paylod to the WebSocket server
        websocket.send(payload)
    finally:
        # Close the WebSocket connection
        websocket.close()


def standalone_receive(ws_uri: str) -> Generator:
    """
    Generator that yields data from a WebSocket.

    Parameters:
    - ws_uri (str): The WebSocket endpoint URI.

    Yields:
    - Any : data received from the WebSocket.
    """
    websocket = create_connection(ws_uri)
    try:
        while True:
            # Receive data from the WebSocket server and yield it
            data = websocket.recv()
            yield data
    finally:
        # Close the WebSocket connection
        websocket.close()
