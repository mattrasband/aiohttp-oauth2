#!/usr/bin/env python3
from pathlib import Path
from typing import Any, Dict

import jinja2
from aiohttp import web
from aiohttp_jinja2 import setup as jinja2_setup, template
from aiohttp_session import SimpleCookieStorage, get_session, setup as session_setup


from aiohttp_oauth2 import oauth2_app


@template("index.html")
async def index(request: web.Request) -> Dict[str, Any]:
    session = await get_session(request)
    return {"user": session.get("user")}


async def logout(request: web.Request):
    session = await get_session(request)
    session.invalidate()
    return web.HTTPTemporaryRedirect(location="/")


async def on_github_login(request: web.Request, github_token):
    session = await get_session(request)

    async with request.app["session"].get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {github_token['access_token']}"},
    ) as r:
        session["user"] = await r.json()

    return web.HTTPTemporaryRedirect(location="/")


def app_factory() -> web.Application:
    app = web.Application()

    jinja2_setup(
        app, loader=jinja2.FileSystemLoader([Path(__file__).parent / "templates"])
    )
    session_setup(app, SimpleCookieStorage())

    app.add_subapp(
        "/auth/github/",
        oauth2_app(
            "a1b8c7904865ac38baba",
            "147d82d8ded7a74899fcc4da2b61f8d305bf81c5",
            "https://github.com/login/oauth/authorize",
            "https://github.com/login/oauth/access_token",
            on_login=on_github_login,
        ),
    )

    app.add_routes([web.get("/", index), web.get("/auth/logout", logout)])

    return app


if __name__ == "__main__":
    web.run_app(app_factory(), host="127.0.0.1")
