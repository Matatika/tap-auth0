"""REST client handling, including Auth0Stream base class."""

import math
from typing import Any, Dict, Optional

import requests
from memoization import cached
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_auth0.auth import Auth0Authenticator


class Auth0Stream(RESTStream):
    """Auth0 stream class."""

    per_page = 100
    include_totals = "true"

    start_jsonpath = "$.start"
    total_jsonpath = "$.total"

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
        params = super().get_url_params(context, next_page_token)
        params["page"] = next_page_token
        params["per_page"] = self.per_page
        params["include_totals"] = self.include_totals
        return params

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Any:
        super().get_next_page_token(response, previous_token)

        json = response.json()
        start = next(iter(extract_jsonpath(self.start_jsonpath, json)))
        total = next(iter(extract_jsonpath(self.total_jsonpath, json)))

        more = start + self.per_page < total

        if more:
            return math.floor((start + self.per_page) / self.per_page)

        return None
