"""Auth0 tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_auth0.streams import (
    Auth0Stream,
    UsersStream,
    GroupsStream,
)

# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    UsersStream,
    GroupsStream,
]


class TapAuth0(Tap):
    """Auth0 tap class."""

    name = "tap-auth0"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            description="App client ID",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            description="App client secret",
        ),
        th.Property(
            "domain",
            th.StringType,
            required=True,
            description="Tenant domain",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
