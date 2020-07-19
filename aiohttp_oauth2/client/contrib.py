# pylint: disable=invalid-name
from functools import partial

from .app import oauth2_app


coinbase = partial(
    oauth2_app,
    authorize_url="https://www.coinbase.com/oauth/authorize",
    token_url="https://api.coinbase.com/oauth/token",
)

digital_ocean = partial(
    oauth2_app,
    authorize_url="https://cloud.digitalocean.com/v1/oauth/authorize",
    token_url="https://cloud.digitalocean.com/v1/oauth/token",
)

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

twitch = partial(
    oauth2_app,
    authorize_url="https://id.twitch.tv/oauth2/authorize",
    token_url="https://id.twitch.tv/oauth2/token",
)
