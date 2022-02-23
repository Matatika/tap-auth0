"""Stream type classes for tap-auth0."""

from singer_sdk.helpers.jsonpath import extract_jsonpath
from typing import Any, Dict, Optional
from urllib.parse import parse_qsl, urlsplit

import requests

from tap_auth0.client import Auth0Stream
from tap_auth0.schemas.user import UserObject


class UsersStream(Auth0Stream):
    """Define users stream."""

    name = "users"
    records_jsonpath = "$.users[*]"
    path = "/users"
    primary_keys = ["user_id"]
    schema = UserObject.schema
