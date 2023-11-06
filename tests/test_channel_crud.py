import random
import string

from tests.conftest import handler
from web_suck_it_py import (
    CreateChannelRequest,
    DeleteChannelRequest,
    GetChannelRequest,
    GetOrCreateChannelRequest,
)


def test_get_channel(handler):
    channel = handler.get_channel(GetChannelRequest(channel_name="do-not-delete-py"))
    assert channel.name == "do-not-delete-py"


def test_get_or_create_channel(handler):
    channel = handler.get_or_create_channel(
        GetOrCreateChannelRequest(channel_name="do-not-delete-py")
    )
    assert channel.name == "do-not-delete-py"


def test_create_and_delete_channel(handler):
    channel_name = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
    )
    channel = handler.create_channel(CreateChannelRequest(channel=channel_name))
    assert channel.name == channel_name
    handler.delete_channel(DeleteChannelRequest(channel_id=channel.id))
