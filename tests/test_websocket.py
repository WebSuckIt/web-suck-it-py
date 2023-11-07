from websockets.sync.client import connect

from tests.conftest import handler
from web_suck_it_py import GetChannelRequest


def test_can_connect_to_url(handler):
    channel = handler.get_channel(GetChannelRequest(channel_name="do-not-delete-py"))
    url = handler.get_connection_url(
        channel_name=channel.name,
        channel_pass_key=channel.pass_key,
        replay_self=True,
    )
    with connect(url) as websocket:
        message = "Hello World From Py"
        websocket.send(message)
        received = websocket.recv()
        assert received == message
