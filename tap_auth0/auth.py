# Copyright (c) 2026 Meltano.

"""Auth0 Authentication."""

import sys

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class Auth0Authenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Auth0."""

    def __init__(self, *, domain: str, client_id: str, client_secret: str) -> None:
        """Create an authenticator for an Auth0 tenant.

        Args:
            domain: Auth0 tenant domain.
            client_id: Client ID of the M2M application.
            client_secret: Client secret of the M2M application.
        """
        super().__init__(
            auth_endpoint=f"https://{domain}/oauth/token",
            client_id=client_id,
            client_secret=client_secret,
        )
        self.audience = f"https://{domain}/api/v2/"

    @property
    @override
    def oauth_request_body(self):
        """Define the OAuth request body for the Auth0 API."""
        return {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
        }
