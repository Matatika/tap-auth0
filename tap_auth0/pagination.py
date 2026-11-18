# Copyright (c) 2026 Meltano.

"""Pagination classes for tap-auth0."""

import sys
from http import HTTPStatus

from singer_sdk.pagination import HeaderLinkPaginator, JSONPathPaginator

if sys.version_info >= (3, 12):
    from typing import override
else:
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
