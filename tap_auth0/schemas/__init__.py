from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.typing import JSONTypeHelper, PropertiesList


class CustomObject(JSONTypeHelper):
    """Base custom object class"""

    properties: PropertiesList

    @classproperty
    def type_dict(cls) -> dict:
        return cls.properties.to_dict()

    @classproperty
    def schema(cls) -> dict:
        return cls.type_dict
