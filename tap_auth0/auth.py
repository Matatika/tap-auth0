"""Auth0 Authentication."""

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
from typing_extensions import Self, override


class Auth0Authenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Auth0."""

    @property
    def domain(self):
        """Auth0 tenant domain."""
        return self.config["domain"]

    @property
    @override
    def auth_endpoint(self):
        return f"https://{self.domain}/oauth/token"

    @property
    @override
    def oauth_request_body(self):
        """Define the OAuth request body for the Auth0 API."""
        return {
            "grant_type": "client_credentials",
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "audience": f"https://{self.domain}/api/v2/",
        }

    @classmethod
    def create_for_stream(cls, stream) -> Self:
        """Create authenticator instance for a stream."""
        return cls(
            stream=stream,
        )
