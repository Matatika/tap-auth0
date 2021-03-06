from singer_sdk.typing import (
    ArrayType,
    BooleanType,
    DateTimeType,
    EmailType,
    IntegerType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
    URIType,
)

from tap_auth0.schemas import CustomObject
from tap_auth0.types import IPType


class _IdentityObject(CustomObject):
    properties = PropertiesList(
        Property("connection", StringType),
        Property("user_id", StringType),
        Property("provider", StringType),
        Property("isSocial", BooleanType),
        Property("profileData", ObjectType()),
    )


class UserObject(CustomObject):
    properties = PropertiesList(
        Property("user_id", StringType),
        Property("email", EmailType),
        Property("email_verified", BooleanType),
        Property("username", StringType),
        Property("phone_number", StringType),
        Property("phone_verified", BooleanType),
        Property("created_at", DateTimeType),
        Property("updated_at", DateTimeType),
        Property("identities", ArrayType(_IdentityObject)),
        Property("app_metadata", ObjectType()),
        Property("user_metadata", ObjectType()),
        Property("picture", URIType),
        Property("name", StringType),
        Property("nickname", StringType),
        Property("multifactor", ArrayType(StringType)),
        Property("last_ip", IPType),
        Property("last_login", DateTimeType),
        Property("logins_count", IntegerType),
        Property("blocked", BooleanType),
        Property("given_name", StringType),
        Property("family_name", StringType),
        Property("last_password_reset", DateTimeType),
        Property("locale", StringType),
    )
