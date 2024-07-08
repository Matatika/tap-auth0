"""Type definitions for refresh token objects."""

import singer_sdk.typing as th
from typing_extensions import override


class RotationTypeType(th.StringType):
    @th.DefaultInstanceProperty
    @override
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "rotating",
                "non-rotating",
            ],
        }


class ExpirationTypeType(th.StringType):
    @th.DefaultInstanceProperty
    @override
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "expiring",
                "non-expiring",
            ],
        }
