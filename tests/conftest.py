from os import getenv
from uuid import UUID

from pytest import fixture

from web_suck_it_py import WebSuckIt


@fixture
def handler() -> WebSuckIt:
    return WebSuckIt(
        user_id=UUID(getenv("USER_ID")),
        access_key=getenv("ACCESS_KEY"),
        public_key=getenv("PUBLIC_KEY"),
    )
