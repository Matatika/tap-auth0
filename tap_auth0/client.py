"""REST client handling, including Auth0Stream base class."""

from typing import Any, Dict, Optional
from urllib.parse import parse_qsl, urlsplit

import requests
from memoization import cached
from singer_sdk.streams import RESTStream

from tap_auth0.auth import Auth0Authenticator


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
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        return dict(parse_qsl(urlsplit(next_page_token).query))

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Any:
        next_link = response.links.get("next")
        if not next_link or not response.json():
            return None

        return next_link["url"]
