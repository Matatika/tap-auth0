"""Pagination classes for tap-auth0."""

from http import HTTPStatus

from singer_sdk.pagination import HeaderLinkPaginator, JSONPathPaginator
from typing_extensions import override


class Auth0Paginator(HeaderLinkPaginator):
    """Base API paginator."""

    @override
    def get_next_url(self, response):
        url = super().get_next_url(response)
        return url if url and response.json() else None


class LogsPaginator(Auth0Paginator):
    """Logs endpoint paginator."""

    @override
    def get_next(self, response):
        return (
            response.status_code == HTTPStatus.BAD_REQUEST
            or super().get_next(response)
            or JSONPathPaginator("$[*].log_id").get_next(response)
        )
