"""Auth0 tap class."""

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_auth0 import streams

STREAM_TYPES = [
    streams.UsersStream,
    streams.ClientsStream,
    streams.LogsStream,
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
        th.Property(
            "job_poll_interval_ms",
            th.IntegerType,
            default=2000,
            description="Job poll interval (ms)",
        ),
        th.Property(
            "job_poll_max_count",
            th.IntegerType,
            default=10,
            description="Maximum job poll count",
        ),
    ).to_dict()

    def discover_streams(self):
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
