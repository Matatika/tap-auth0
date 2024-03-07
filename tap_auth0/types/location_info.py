"""Type definitions for location info objects."""

import singer_sdk.typing as th
from typing_extensions import override


class ContinentCodeType(th.StringType):
    @th.DefaultInstanceProperty
    @override
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "AF",  # Africa
                "AN",  # Antarctica
                "AS",  # Asia
                "EU",  # Europe
                "NA",  # North America
                "OC",  # Oceania
                "SA",  # South America
            ],
        }
