from singer_sdk.typing import (
    ArrayType,
    BooleanType,
    DateTimeType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
)

from tap_auth0.schemas import CustomObject
from tap_auth0.types import IPType
from tap_auth0.types.location_info import ContinentCodeType
from tap_auth0.types.log import LogTypeType


class _LocationInfoObject(CustomObject):
    properties = PropertiesList(
        Property("country_code", StringType),
        Property("country_code3", StringType),
        Property("country_name", StringType),
        Property("city_name", StringType),
        Property("latitude", StringType),
        Property("longitude", StringType),
        Property("time_zone", StringType),
        Property("continent_code", ContinentCodeType),
    )


class _Auth0ClientObject(CustomObject):
    properties = PropertiesList(
        Property("name", StringType),
        Property("version", StringType),
    )


class LogObject(CustomObject):
    properties = PropertiesList(
        Property("date", DateTimeType),
        Property("type", LogTypeType),
        Property("description", StringType),
        Property("connection", StringType),
        Property("connection_id", StringType),
        Property("client_id", StringType),
        Property("client_name", StringType),
        Property("ip", IPType),
        Property("hostname", StringType),
        Property("user_id", StringType),
        Property("user_name", StringType),
        Property("audience", StringType),
        Property("scope", ArrayType(StringType)),
        Property("strategy", StringType),
        Property("strategy_type", StringType),
        Property("log_id", StringType),
        Property("isMobile", BooleanType),
        Property("details", ObjectType()),
        Property("user_agent", StringType),
        Property("location_info", _LocationInfoObject),
        Property("auth0_client", _Auth0ClientObject),
        Property("_id", StringType),
        Property("session_connection", StringType),
        Property("client_ip", IPType),
    )
