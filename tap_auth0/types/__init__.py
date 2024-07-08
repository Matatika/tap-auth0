"""Type definitions for tap-auth0."""

from __future__ import annotations

import itertools

import singer_sdk.typing as th
from typing_extensions import override


class IPType(th.JSONTypeHelper):
    ip_types = (th.IPv4Type, th.IPv6Type)

    @th.DefaultInstanceProperty
    @override
    def type_dict(cls):
        type_dicts: list[dict] = [ip_type.type_dict for ip_type in cls.ip_types]

        return {
            "type": list(set(itertools.chain(*[td.pop("type") for td in type_dicts]))),
            "oneOf": type_dicts,
        }
