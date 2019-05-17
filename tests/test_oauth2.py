from aiohttp import web
from yarl import URL


class TestAuthView:
    async def test_redirect(self, client):
        resp = await client.get("/auth", allow_redirects=False)
        assert resp.status == 307
        to = URL(resp.headers["location"])
        assert str(to).startswith(client.server.app["AUTHORIZE_URL"])
        assert {"client_id", "redirect_uri"} == set(to.query.keys())

    async def test_redirect_scopes(self, client):
        client.server.app["SCOPES"] = ["foo", "bar"]
        resp = await client.get("/auth", allow_redirects=False)
        assert resp.status == 307
        to = URL(resp.headers["location"])
        assert {"client_id", "redirect_uri", "scope"} == set(to.query.keys())
        assert to.query["scope"] == "foo bar"


class TestCallbackView:
    async def test_default_error_handler(self, client):
        resp = await client.get("/callback", params={"error": "oops"})
        assert resp.status == 500

    async def test_custom_error_handler(self, client):
        async def on_error(request):
            return web.HTTPTemporaryRedirect(location="/other/page")

        client.server.app["ON_ERROR"] = on_error

        resp = await client.get("/callback", params={"error": "oops"}, allow_redirects=False)
        assert resp.status == 307
        assert resp.headers["location"].endswith("/other/page")

    async def test_exchange_code(self, client):
        pass

    async def test_exchange_code_custom_handler(self, client):
        pass
