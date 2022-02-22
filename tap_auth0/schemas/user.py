from singer_sdk.typing import (
    PropertiesList,
    Property,
    ArrayType,
    BooleanType,
    DateTimeType,
    IntegerType,
    ObjectType,
    StringType,
)

from tap_auth0.schemas import CustomObject


class _IdentityObject(CustomObject):
    properties = PropertiesList(
        Property("connection", StringType),
        Property("user_id", StringType),
        Property("provider", StringType),
        Property("isSocial", BooleanType),
    )


class UserObject(CustomObject):
    properties = PropertiesList(
        Property("user_id", StringType),
        Property("email", StringType),
        Property("email_verified", BooleanType),
        Property("username", StringType),
        Property("phone_number", StringType),
        Property("phone_verified", BooleanType),
        Property("created_at", DateTimeType),
        Property("updated_at", DateTimeType),
        Property("identities", ArrayType(_IdentityObject)),
        Property("app_metadata", ObjectType()),
        Property("user_metadata", ObjectType()),
        Property("picture", StringType),
        Property("name", StringType),
        Property("nickname", StringType),
        Property("multifactor", ArrayType(StringType)),
        Property("last_ip", StringType),
        Property("last_login", DateTimeType),
        Property("logins_count", IntegerType),
        Property("blocked", BooleanType),
        Property("given_name", StringType),
        Property("family_name", StringType),
    )
