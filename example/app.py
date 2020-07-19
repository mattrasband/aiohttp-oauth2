#!/usr/bin/env python3
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import jinja2
from aiohttp import web
from aiohttp_jinja2 import setup as jinja2_setup, template
from aiohttp_session import SimpleCookieStorage, get_session, setup as session_setup
from aiohttp_oauth2.client.contrib import (
    coinbase,
    digital_ocean as digitalocean,
    github,
    google,
    twitch,
)


@dataclass
class SocialUser:
    name: str
    id: str
    img: str


@dataclass
class Provider:
    func: Callable
    name: str
    on_login: Callable[[web.Request, Any], web.Response]
    scopes: Optional[List[str]] = field(default_factory=list)

    def __str__(self) -> str:
        return self.name

    @property
    def url(self) -> str:
        return f"/auth/{self}"

    @property
    def client_id(self) -> str:
        return os.getenv(f"{self}_CLIENT_ID".upper())

    @property
    def client_secret(self) -> str:
        return os.getenv(f"{self}_CLIENT_SECRET".upper())


async def on_coinbase_login(request: web.Request, access_token):
    session = await get_session(request)

    async with request.app["session"].get(
        "https://api.coinbase.com/v2/user",
        headers={
            "Authorization": f"Bearer {access_token['access_token']}",
            "CB-VERSION": "2019-11-15",
        },
    ) as r:
        body = (await r.json())["data"]
        session["coinbase_user"] = asdict(SocialUser(
                name=body["name"],
                img=body["avatar_url"],
                id=body["id"],
        ))

    return web.HTTPTemporaryRedirect(location="/")


async def on_digitalocean_login(request: web.Request, access_token):
    session = await get_session(request)

    session["digitalocean_user"] = asdict(SocialUser(
        name=access_token["info"]["name"],
        img="",
        id=access_token["info"]["uuid"],
    ))

    return web.HTTPTemporaryRedirect(location="/")


async def on_github_login(request: web.Request, github_token):
    session = await get_session(request)

    async with request.app["session"].get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {github_token['access_token']}"},
    ) as r:
        user = await r.json()
        session["github_user"] = asdict(SocialUser(
                id=user["id"],
                name=user["login"],
                img=user["avatar_url"],
        ))

    return web.HTTPTemporaryRedirect(location="/")


async def on_google_login(request: web.Request, google_token: str):
    session = await get_session(request)

    async with request.app["session"].get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {google_token['access_token']}"},
    ) as r:
        google_user = await r.json()
        session["google_user"] = asdict(SocialUser(
            id=google_user["sub"],
            img=google_user["picture"],
            name=google_user["name"],
        ))

    return web.HTTPTemporaryRedirect(location="/")


async def on_twitch_login(request: web.Request, access_token):
    session = await get_session(request)

    async with request.app["session"].get(
        "https://api.twitch.tv/helix/users",
        headers={
            "Authorization": f"Bearer {access_token['access_token']}",
            "Client-ID": os.getenv("TWITCH_CLIENT_ID"),
        },
    ) as r:
        twitch_user = (await r.json())["data"][0]
        session["twitch_user"] = asdict(SocialUser(
            id=twitch_user["id"],
            name=twitch_user["login"],
            img=twitch_user["profile_image_url"],
        ))

    return web.HTTPTemporaryRedirect(location="/")


async def app_factory() -> web.Application:
    app = web.Application()

    providers = [
        Provider(coinbase, "coinbase", on_coinbase_login, ["wallet:user:read"]),
        Provider(digitalocean, "digitalocean", on_digitalocean_login),
        Provider(github, "github", on_github_login),
        Provider(google, "google", on_google_login, ["profile", "email"]),
        Provider(twitch, "twitch", on_twitch_login),
    ]

    jinja2_setup(
        app,
        loader=jinja2.FileSystemLoader([Path(__file__).parent / "templates"]),
        extensions=["jinja2.ext.with_"],
    )
    session_setup(app, SimpleCookieStorage())

    for provider in providers[:]:
        if provider.client_id and provider.client_secret:
            print("Adding provider", provider)
            app.add_subapp(
                provider.url,
                provider.func(provider.client_id, provider.client_secret, on_login=provider.on_login, scopes=provider.scopes or [])
            )
        else:
            providers.remove(provider)
            print("Missing credentials for", provider)

    app["providers"] = providers

    app.add_routes([
        web.get("/", index),
        web.get("/auth/logout", logout),
    ])

    return app


@template("index.html")
async def index(request: web.Request) -> Dict[str, Any]:
    session = await get_session(request)

    context = {
        "users": {},
        "providers": request.app["providers"],
    }

    for provider in request.app["providers"]:
        social_user = None
        if (u := session.get(f"{provider}_user")):
            social_user = SocialUser(**u)
        context["users"][str(provider)] = social_user

    return context


async def logout(request: web.Request):
    session = await get_session(request)
    if (provider := request.query.get("provider")):
        session.pop(f"{provider}_user")
    else:
        session.invalidate()
    return web.HTTPTemporaryRedirect(location="/")


if __name__ == "__main__":
    web.run_app(app_factory(), host="0.0.0.0", port=8080)
