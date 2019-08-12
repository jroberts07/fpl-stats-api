import pytest
from sanic.websocket import WebSocketProtocol

from server import app as sanic_app


@pytest.fixture
def test_cli(loop, sanic_client):
    """Used to create a fresh event loop and sanic app for each test.

    Args:
        loop (obj): The event loop.
        sanic_client (obj): The sanic app object.

    Returns:
        obj: Event loop.
    """
    return loop.run_until_complete(
        sanic_client(sanic_app, protocol=WebSocketProtocol))
