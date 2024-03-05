"""REST client handling, including Auth0Stream base class."""

from functools import cached_property
from typing import Optional, Union
from urllib.parse import ParseResult, parse_qsl

from singer_sdk.streams import RESTStream

from tap_auth0.auth import Auth0Authenticator
from tap_auth0.pagination import Auth0Paginator


class Auth0Stream(RESTStream):
    """Auth0 stream class."""

    @property
    def url_base(self):
        domain = self.config["domain"]
        return f"https://{domain}/api/v2"

    @cached_property
    def authenticator(self):
        return Auth0Authenticator.create_for_stream(self)

    def get_url_params(
        self,
        context,
        next_page_token: Optional[Union[str, ParseResult]],
    ):
        params = super().get_url_params(context, next_page_token)

        try:
            return dict(parse_qsl(next_page_token.query))
        except AttributeError:
            return params

    def get_new_paginator(self):
        return Auth0Paginator()

    def backoff_max_tries(self):
        return 8
