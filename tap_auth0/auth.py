"""Auth0 Authentication."""

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


class Auth0Authenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Auth0."""

    @property
    def domain(self) -> str:
        return self.config["domain"]

    @property
    def auth_endpoint(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Auth0 API."""
        return {
            "grant_type": "client_credentials",
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "audience": f"https://{self.domain}/api/v2/",
        }

    @classmethod
    def create_for_stream(cls, stream) -> "Auth0Authenticator":
        return cls(
            stream=stream,
        )
