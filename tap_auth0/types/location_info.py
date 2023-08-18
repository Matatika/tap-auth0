from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.typing import StringType


class ContinentCodeType(StringType):
    @classproperty
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
