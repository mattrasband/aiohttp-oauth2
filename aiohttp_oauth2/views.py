from aiohttp import web
from yarl import URL

routes = web.RouteTableDef()


def redirect_uri(request):
    return str(
        request.url.with_path(str(request.app.router["callback"].url_for()))
    )


@routes.view("/auth", name="auth")
class AuthView(web.View):
    """
    View to kick off the oauth2 flow, this simply redirects the
    client to the oauth2 providers authorization endpoint
    """
    async def get(self) -> web.Response:
        params = {
            "client_id": self.request.app["CLIENT_ID"],
            "redirect_uri": redirect_uri(self.request),
            # "state": TODO
        }

        if self.request.app["SCOPES"]:
            params["scope"] = " ".join(self.request.app["SCOPES"])

        location = str(
            URL(self.request.app["AUTHORIZE_URL"]).with_query(params)
        )

        return web.HTTPTemporaryRedirect(location=location)


@routes.view("/callback", name="callback")
class CallbackView(web.View):
    """
    Handle the oauth2 callback
    """
    async def get(self) -> web.Response:
        if self.request.query.get("error") is not None:
            return self.request.app.get("ON_ERROR", self.on_error)

        async with self.request.app["session"].post(
            self.request.app["TOKEN_URL"],
            headers={
                "Accept": "application/json",
            },
            json={
                "client_id": self.request.app["CLIENT_ID"],
                "client_secret": self.request.app["CLIENT_SECRET"],
                "code": self.request.query["code"],
                "redirect_uri": redirect_uri(self.request),
            },
        ) as r:
            result = await r.json()

        on_login = self.request.app.get("ON_LOGIN", self.on_login)
        return await on_login(self.request, result)

    async def on_login(self, request, result):
        return web.json_response(result)

    async def on_error(self, request, error):
        raise web.HTTPServerError()
