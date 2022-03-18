from typing import List

from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.typing import IPv4Type, IPv6Type, StringType


class IPType(IPv4Type, IPv6Type):
    @classproperty
    def type_dict(cls):
        cls.__bases__: List[StringType]

        types = set()
        type_dicts = []

        for base in cls.__bases__:
            type_dict = base.type_dict

            types.update(type_dict.pop("type"))
            type_dicts.append(type_dict)

        return {
            "type": list(types),
            "oneOf": type_dicts,
        }
