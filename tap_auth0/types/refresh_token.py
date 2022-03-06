from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.typing import StringType


class RotationTypeType(StringType):
    @classproperty
    def type_dict(cls) -> dict:
        return {
            **super().type_dict,
            "enum": [
                "rotating",
                "non-rotating",
            ],
        }


class ExpirationTypeType(StringType):
    @classproperty
    def type_dict(cls) -> dict:
        return {
            **super().type_dict,
            "enum": [
                "expiring",
                "non-expiring",
            ],
        }
