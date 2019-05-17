import pytest

from aiohttp_oauth2 import oauth2_app


@pytest.fixture
def client(loop, aiohttp_client):
    return loop.run_until_complete(
        aiohttp_client(
            oauth2_app(
                client_id="123",
                client_secret="456",
                authorize_url="http://localhost/o/authorize",
                token_url="http://localhost/o/token",
                #  scopes: Optional[List[str]] = None,
                #  on_login: Optional[Callable[[web.Request, Dict[str, Any]], web.Response]] = None,
                #  on_error: Optional[Callable[[web.Request, str], web.Response]] = None,
            )
        )
    )
