"""Stream type classes for tap-auth0."""

from tap_auth0.client import Auth0Stream
from tap_auth0.schemas.client import ClientObject
from tap_auth0.schemas.user import UserObject


class UsersStream(Auth0Stream):
    """Define users stream."""

    name = "users"
    records_jsonpath = "$.users[*]"
    path = "/users"
    primary_keys = ["user_id"]
    schema = UserObject.schema


class ClientsStream(Auth0Stream):
    """Define clients stream."""

    name = "clients"
    records_jsonpath = "$.clients[*]"
    path = "/clients"
    primary_keys = ["client_id"]
    schema = ClientObject.schema
