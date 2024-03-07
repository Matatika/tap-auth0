"""Schema definitions for log objects."""

from singer_sdk import typing as th

from tap_auth0.schemas import CustomObject
from tap_auth0.types import IPType
from tap_auth0.types.location_info import ContinentCodeType
from tap_auth0.types.log import LogTypeType


class _LocationInfoObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("country_code", th.StringType),
        th.Property("country_code3", th.StringType),
        th.Property("country_name", th.StringType),
        th.Property("city_name", th.StringType),
        th.Property("latitude", th.StringType),
        th.Property("longitude", th.StringType),
        th.Property("time_zone", th.StringType),
        th.Property("continent_code", ContinentCodeType),
    )


class _Auth0ClientObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("version", th.StringType),
    )


class LogObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("date", th.DateTimeType),
        th.Property("type", LogTypeType),
        th.Property("description", th.StringType),
        th.Property("connection", th.StringType),
        th.Property("connection_id", th.StringType),
        th.Property("client_id", th.StringType),
        th.Property("client_name", th.StringType),
        th.Property("ip", IPType),
        th.Property("hostname", th.StringType),
        th.Property("user_id", th.StringType),
        th.Property("user_name", th.StringType),
        th.Property("audience", th.StringType),
        th.Property("scope", th.ArrayType(th.StringType)),
        th.Property("strategy", th.StringType),
        th.Property("strategy_type", th.StringType),
        th.Property("log_id", th.StringType),
        th.Property("isMobile", th.BooleanType),
        th.Property("details", th.ObjectType()),
        th.Property("user_agent", th.StringType),
        th.Property("location_info", _LocationInfoObject),
        th.Property("auth0_client", _Auth0ClientObject),
        th.Property("_id", th.StringType),
        th.Property("session_connection", th.StringType),
        th.Property("client_ip", IPType),
    )
