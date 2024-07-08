"""Type definitions for JWT configuration objects."""

import singer_sdk.typing as th
from typing_extensions import override


class AlgType(th.StringType):
    @th.DefaultInstanceProperty
    @override
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "HS256",
                "RS256",
            ],
        }
