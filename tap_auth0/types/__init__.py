from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.typing import JSONTypeHelper


class EmailType(JSONTypeHelper):
    @classproperty
    def type_dict(cls) -> dict:
        return {
            "type": ["string"],
            "format": ["email"],
        }


class IPv4Type(JSONTypeHelper):
    @classproperty
    def type_dict(cls) -> dict:
        return {
            "type": ["string"],
            "format": ["ipv4"],
        }


class URIType(JSONTypeHelper):
    @classproperty
    def type_dict(cls) -> dict:
        return {
            "type": ["string"],
            "format": ["uri"],
        }
