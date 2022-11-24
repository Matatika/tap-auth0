from typing import Callable

from requests import Response
from singer_sdk.pagination import HeaderLinkPaginator, JSONPathPaginator


class Auth0Paginator(HeaderLinkPaginator):
    def get_next_url(self, response: Response):
        url = super().get_next_url(response)
        return url if url and response.json() else None


class LogsPaginator(Auth0Paginator):
    def __init__(
        self,
        log_expired_callback: Callable[[Response], bool],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.log_expired_callback = log_expired_callback

    def get_next(self, response: Response):
        return (
            self.log_expired_callback(response)
            or super().get_next(response)
            or JSONPathPaginator("$[*].log_id").get_next(response)
        )
