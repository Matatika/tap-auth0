from singer_sdk.typing import (
    BooleanType,
    DateTimeType,
    IPv4Type,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
)

from tap_auth0.schemas import CustomObject
from tap_auth0.types.location_info import ContinentCodeType


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
        Property("type", StringType),
        Property("description", StringType),
        Property("connection", StringType),
        Property("connection_id", StringType),
        Property("client_id", StringType),
        Property("client_name", StringType),
        Property("ip", IPv4Type),
        Property("hostname", IPv4Type),
        Property("user_id", StringType),
        Property("user_name", StringType),
        Property("audience", StringType),
        Property("scope", StringType),
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
        Property("client_ip", IPv4Type),
    )
