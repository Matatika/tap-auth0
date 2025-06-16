"""Schema definitions for tap-auth0."""

from singer_sdk import typing as th

IPType = th.OneOf(th.IPv4Type, th.IPv6Type, th.CustomType({"type": ["null"]}))
