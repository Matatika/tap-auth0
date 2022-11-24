"""REST client handling, including Auth0Stream base class."""

from typing import Any, Dict, Optional, Union
from urllib.parse import ParseResult, parse_qsl

from memoization import cached
from singer_sdk.streams import RESTStream

from tap_auth0.auth import Auth0Authenticator
from tap_auth0.pagination import Auth0Paginator


class Auth0Stream(RESTStream):
    """Auth0 stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        domain = self.config["domain"]
        return f"https://{domain}/api/v2"

    @property
    @cached
    def authenticator(self) -> Auth0Authenticator:
        """Return a new authenticator object."""
        return Auth0Authenticator.create_for_stream(self)

    def get_url_params(
        self,
        context: Optional[dict],
        next_page_token: Optional[Union[str, ParseResult]],
    ) -> Dict[str, Any]:
        try:
            return dict(parse_qsl(next_page_token.query))
        except AttributeError:
            return {}

    def get_new_paginator(self):
        return Auth0Paginator()
