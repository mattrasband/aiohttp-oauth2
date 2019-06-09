# pylint: disable=invalid-name
from functools import partial

from .app import oauth2_app


github = partial(
    oauth2_app,
    authorize_url="https://github.com/login/oauth/authorize",
    token_url="https://github.com/login/oauth/access_token",
)

google = partial(
    oauth2_app,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    token_url="https://www.googleapis.com/oauth2/v4/token",
)

slack = partial(
    oauth2_app,
    authorize_url="https://slack.com/oauth/authorize",
    token_url="https://slack.com/api/oauth.access",
    json_data=False,
)

twitter = partial(
    oauth2_app,
    authorize_url="https://api.twitter.com/oauth/authorize",
    token_url="https://api.twitter.com/oauth2/token",
)
