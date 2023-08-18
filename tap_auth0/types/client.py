from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.typing import StringType


class AppTypeType(StringType):
    @classproperty
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "spa",
                "native",
                "non_interactive",
                "regular_web",
            ],
        }


class GrantTypeType(StringType):
    @classproperty
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "authorization_code",
                "implicit",
                "refresh_token",
                "client_credentials",
                "password",
                "http://auth0.com/oauth/grant-type/password-realm",
                "http://auth0.com/oauth/grant-type/mfa-oob",
                "http://auth0.com/oauth/grant-type/mfa-otp",
                "http://auth0.com/oauth/grant-type/mfa-recovery-code",
                "urn:ietf:params:oauth:grant-type:device_code",
            ],
        }


class TokenEndpointAuthMethodType(StringType):
    @classproperty
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "none",
                "client_secret_post",
                "client_secret_basic",
            ],
        }


class OrganizationUsageType(StringType):
    @classproperty
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "deny",
                "allow",
                "require",
            ],
        }


class OrganizationRequireBehaviourType(StringType):
    @classproperty
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "no_prompt",
                "pre_login_prompt",
            ],
        }
