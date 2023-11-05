from pytest import fixture

from web_suck_it_py import WebSuckIt
from uuid import UUID
from os import getenv

@fixture
def get_handler() -> WebSuckIt:
    return WebSuckIt(
        user_id=UUID(getenv('USER_ID')),
        access_key=getenv('ACCESS_KEY'),
        public_key=getenv('PUBLIC_KEY'),
    )
