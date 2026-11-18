# Copyright (c) 2026 Meltano.

"""REST client handling, including Auth0Stream base class."""

from __future__ import annotations

import sys
from functools import cached_property
from urllib.parse import ParseResult, parse_qsl

from singer_sdk.exceptions import RetriableAPIError
from singer_sdk.streams import RESTStream

from tap_auth0.auth import Auth0Authenticator
from tap_auth0.pagination import Auth0Paginator

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


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
        return Auth0Authenticator(
            domain=self.config["domain"],
            client_id=self.config["client_id"],
            client_secret=self.config["client_secret"],
        )

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
    def backoff_wait_generator(self):
        expo = super().backoff_wait_generator()
        next(expo)
        exception = yield

        while True:
            if (
                isinstance(exception, RetriableAPIError)
                and exception.response is not None
                and "Retry-After" in exception.response.headers
            ):
                exception = yield float(exception.response.headers["Retry-After"])
            else:
                exception = yield next(expo)

    @override
    def backoff_max_tries(self):
        return 8
