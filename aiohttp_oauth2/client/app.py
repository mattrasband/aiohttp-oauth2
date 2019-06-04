from typing import Any, Callable, Dict, List, Optional

from aiohttp import ClientSession, web

from .views import routes


async def client_session(app: web.Application):
    async with ClientSession() as session:
        app["session"] = session
        yield


def oauth2_app(  # pylint: disable=too-many-arguments
    client_id: str,
    client_secret: str,
    authorize_url: str,
    token_url: str,
    scopes: Optional[List[str]] = None,
    on_login: Optional[Callable[[web.Request, Dict[str, Any]], web.Response]] = None,
    on_error: Optional[Callable[[web.Request, str], web.Response]] = None,
    json_data=True,
) -> web.Application:
    """
    Factory to generate an aiohttp application configured as an oauth2 client.
    """
    app = web.Application()

    app.update(  # pylint: disable=no-member
        CLIENT_ID=client_id,
        CLIENT_SECRET=client_secret,
        AUTHORIZE_URL=authorize_url,
        TOKEN_URL=token_url,
        SCOPES=scopes,
        ON_LOGIN=on_login,
        ON_ERROR=on_error,
        DATA_AS_JSON=json_data,
    )
    app.cleanup_ctx.append(client_session)

    app.add_routes(routes)

    return app
