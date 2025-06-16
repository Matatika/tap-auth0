"""Schema definitions for tap-auth0."""

from singer_sdk import typing as th

IPType = th.CustomType(
    th.StringType().to_dict() | th.OneOf(th.IPv4Type, th.IPv6Type).to_dict()
)
