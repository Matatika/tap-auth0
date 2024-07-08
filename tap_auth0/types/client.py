"""Type definitions for client objects."""

import singer_sdk.typing as th
from typing_extensions import override


class AppTypeType(th.StringType):
    @th.DefaultInstanceProperty
    @override
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


class GrantTypeType(th.StringType):
    @th.DefaultInstanceProperty
    @override
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


class TokenEndpointAuthMethodType(th.StringType):
    @th.DefaultInstanceProperty
    @override
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "none",
                "client_secret_post",
                "client_secret_basic",
            ],
        }


class OrganizationUsageType(th.StringType):
    @th.DefaultInstanceProperty
    @override
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "deny",
                "allow",
                "require",
            ],
        }


class OrganizationRequireBehaviourType(th.StringType):
    @th.DefaultInstanceProperty
    @override
    def type_dict(cls):
        return {
            **super().type_dict,
            "enum": [
                "no_prompt",
                "pre_login_prompt",
            ],
        }
