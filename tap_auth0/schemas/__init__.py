from singer_sdk import typing as th
from singer_sdk.helpers._classproperty import classproperty


class CustomObject(th.JSONTypeHelper):
    """Base custom object class"""

    properties: th.PropertiesList

    @classproperty
    def type_dict(cls):
        return cls.properties.to_dict()

    @classproperty
    def schema(cls):
        return cls.type_dict
