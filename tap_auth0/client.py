"""REST client handling, including Auth0Stream base class."""

from __future__ import annotations

from functools import cached_property
from urllib.parse import ParseResult, parse_qsl

from singer_sdk.streams import RESTStream
from typing_extensions import override

from tap_auth0.auth import Auth0Authenticator
from tap_auth0.pagination import Auth0Paginator


class Auth0Stream(RESTStream):
    """Auth0 stream class."""

    @property
    @override
    def url_base(self):
        domain = self.config["domain"]
        return f"https://{domain}/api/v2"

    @cached_property
    @override
    def authenticator(self):
        return Auth0Authenticator.create_for_stream(self)

    @override
    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)

        if isinstance(next_page_token, ParseResult):
            return dict(parse_qsl(next_page_token.query))

        return params

    @override
    def get_new_paginator(self):
        return Auth0Paginator()

    @override
    def backoff_max_tries(self):
        return 8
