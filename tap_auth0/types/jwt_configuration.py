from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.typing import StringType


class AlgType(StringType):
    @classproperty
    def type_dict(cls) -> dict:
        return {
            **super().type_dict,
            "enum": [
                "HS256",
                "RS256",
            ],
        }
