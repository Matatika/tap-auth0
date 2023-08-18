from requests import Response
from singer_sdk.pagination import HeaderLinkPaginator, JSONPathPaginator


class Auth0Paginator(HeaderLinkPaginator):
    def get_next_url(self, response: Response):
        url = super().get_next_url(response)
        return url if url and response.json() else None


class LogsPaginator(Auth0Paginator):
    def get_next(self, response: Response):
        return (
            response.status_code == 400
            or super().get_next(response)
            or JSONPathPaginator("$[*].log_id").get_next(response)
        )
