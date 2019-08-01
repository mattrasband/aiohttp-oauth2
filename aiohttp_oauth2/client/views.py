from aiohttp import web
from yarl import URL

routes = web.RouteTableDef()  # pylint: disable=invalid-name


def redirect_uri(request):
    return str(request.url.with_path(str(request.app.router["callback"].url_for())))


@routes.view("/auth", name="auth")
class AuthView(web.View):
    """
    View to kick off the oauth2 flow, this simply redirects the
    client to the oauth2 provider's authorization endpoint
    """

    async def get(self) -> web.Response:
        params = {
            "client_id": self.request.app["CLIENT_ID"],
            "redirect_uri": redirect_uri(self.request),
            "response_type": "code",
            # "state": TODO
            **self.request.app["AUTH_EXTRAS"],
        }

        if self.request.app["SCOPES"]:
            params["scope"] = " ".join(self.request.app["SCOPES"])

        location = str(URL(self.request.app["AUTHORIZE_URL"]).with_query(params))

        return web.HTTPTemporaryRedirect(location=location)


@routes.view("/callback", name="callback")
class CallbackView(web.View):
    """
    Handle the oauth2 callback
    """

    async def get(self) -> web.Response:
        if self.request.query.get("error") is not None:
            return await self.handle_error(self.request, self.request.query["error"])

        params = {"headers": {"Accept": "application/json"}}
        body = {
            "client_id": self.request.app["CLIENT_ID"],
            "client_secret": self.request.app["CLIENT_SECRET"],
            "code": self.request.query["code"],
            "redirect_uri": redirect_uri(self.request),
            "grant_type": "authorization_code",
        }
        if self.request.app["DATA_AS_JSON"]:
            params["json"] = body
        else:
            params["data"] = body

        async with self.request.app["session"].post(
            self.request.app["TOKEN_URL"], **params
        ) as r:  # pylint: disable=invalid-name
            result = await r.json()

        return await self.handle_success(self.request, result)

    async def handle_error(self, request: web.Request, error: str):
        handler = request.app.get("ON_ERROR")
        if handler is not None:
            return await handler(request)
        raise web.HTTPInternalServerError(text=f"Unhandled OAuth2 Error: {error}")

    async def handle_success(self, request, user_data):
        handler = request.app.get("ON_LOGIN")
        if handler is not None:
            return await handler(self.request, user_data)
        return web.json_response(user_data)
