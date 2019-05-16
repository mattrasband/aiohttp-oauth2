# aiohttp-oauth2

A provider agnostic oauth2 client library for aiohttp, implemented as a self-composed nested application.

No opinions about auth mechanisms are enforced on the application, an `on_login` and `on_error` coroutine can be provided to implement your own login mechanisms (token, session, etc).

## Usage

### Simple

```python
from aiohttp import web

from aiohttp_oauth2 import oauth2_app


async def app_factory():
    app = web.Application()

    app.add_subapp(
        "/github/",  # any arbitrary prefix
        oauth2_app(
            client_id=123,
            client_secret=456,
            authorize_url="https://github.com/login/oauth/authorize",
            token_url="https://github.com/login/oauth/access_token",
            # add scopes if you want to customize them
            scopes=["foo", "bar", "baz"],
            # optionally add an on_login coroutine to handle the post-login logic
            # it should expect the request and the oauth2 access code response
            on_login=set_session_and_redirect,
            on_error=show_error_page,
        ),
    )

    return app
```

The necessary oauth2 routes are added as `/auth` and `/callback`, only the former a developer needs to worry about.

Now logging in a user is as simple as redirecting them to: `/github/auth`.

### Complex

Since the `oauth2_app` function is simply a factory that generates sub-apps, you can use this to add any number of oauth2 providers to log in against:

```python

async def app_factory():
    app = web.Application()

    app.add_subapp(
        "/github/",
        oauth2_app(
            ...,
            authorize_url="https://github.com/login/oauth/authorize",
            token_url="https://github.com/login/oauth/access_token",
        )
    )
    app.add_subapp(
        "/github/",
        oauth2_app(
            ...,
            authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
            token_url="https://www.googleapis.com/oauth2/v4/token",
        )
    )
    app.add_subapp(
        "/twitter/",
        oauth2_app(
            ...,
            authorize_url="https://api.twitter.com/oauth/authorize",
            token_url="https://api.twitter.com/oauth2/token",
        )
    )

    ...

    return app
```

### Examples

Check the "examples" directory for working examples:

```
$ cd examples
$ pip install -r requirements.txt

# this just makes the library available for import, don't typically do it :D
$ PYTHONPATH=".." python github.py
```
