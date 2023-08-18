from singer_sdk import typing as th

from tap_auth0.schemas import CustomObject
from tap_auth0.types import IPType


class _IdentityObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("connection", th.StringType),
        th.Property("user_id", th.StringType),
        th.Property("provider", th.StringType),
        th.Property("isSocial", th.BooleanType),
        th.Property("profileData", th.ObjectType()),
    )


class UserObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("user_id", th.StringType),
        th.Property("email", th.EmailType),
        th.Property("email_verified", th.BooleanType),
        th.Property("username", th.StringType),
        th.Property("phone_number", th.StringType),
        th.Property("phone_verified", th.BooleanType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("identities", th.ArrayType(_IdentityObject)),
        th.Property("app_metadata", th.ObjectType()),
        th.Property("user_metadata", th.ObjectType()),
        th.Property("picture", th.URIType),
        th.Property("name", th.StringType),
        th.Property("nickname", th.StringType),
        th.Property("multifactor", th.ArrayType(th.StringType)),
        th.Property("last_ip", IPType),
        th.Property("last_login", th.DateTimeType),
        th.Property("logins_count", th.IntegerType),
        th.Property("blocked", th.BooleanType),
        th.Property("given_name", th.StringType),
        th.Property("family_name", th.StringType),
        th.Property("last_password_reset", th.DateTimeType),
        th.Property("locale", th.StringType),
    )
