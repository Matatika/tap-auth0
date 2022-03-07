"""Stream type classes for tap-auth0."""

import gzip
import json
import time
from typing import Any, Dict, Iterable

import ndjson
import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath

from tap_auth0.client import Auth0Stream
from tap_auth0.schemas.client import ClientObject
from tap_auth0.schemas.user import UserObject


class UsersStream(Auth0Stream):
    """Define users stream."""

    name = "users"
    primary_keys = ["user_id"]
    schema = UserObject.schema
    authenticator = None
    url_base = ""

    job_poll_interval_ms = 2000
    job_poll_max_count = 10

    def get_url_params(self, *args, **kwargs) -> None:
        return None

    # since Auth0 restricts the total number of users returned from the get users
    # endpoint to 1000 (including paging), we need to create a user export job in order
    # to bypass this limitation
    #
    # https://auth0.com/docs/manage-users/user-search/retrieve-users-with-get-users-endpoint#limitations
    def get_records(self, *args, **kwargs) -> Iterable[Dict[str, Any]]:
        authenticator = super().authenticator
        url_base = super().url_base

        session = requests.Session()
        session.headers = authenticator.auth_headers
        session.params = authenticator.auth_params

        # create export users job
        # https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
        self.path = "/jobs/users-exports"
        create_export_users_job_request = session.prepare_request(
            requests.Request(
                "POST",
                url_base + self.path,
                json={
                    "format": "json",
                    "fields": [{"name": name} for name in self.schema["properties"]],
                },
            )
        )

        export_users_job = self._request(create_export_users_job_request, None)
        job_id = export_users_job.json()["id"]

        # poll export users job
        # https://auth0.com/docs/api/management/v2#!/Jobs/get_jobs_by_id
        self.path = f"/jobs/{job_id}"
        get_export_users_job_request = session.prepare_request(
            requests.Request(
                "GET",
                url_base + self.path,
            ),
        )

        export_users_job = self._poll_job(get_export_users_job_request)
        self.path = export_users_job["location"]

        return super().get_records(*args, **kwargs)

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        users = gzip.decompress(response.content)
        users_ndjson = json.loads(users, cls=ndjson.Decoder)

        yield from extract_jsonpath(self.records_jsonpath, users_ndjson)

    def get_next_page_token(self, *args, **kwargs) -> None:
        return None

    def _poll_job(self, get_job_request: requests.PreparedRequest, count=1) -> Any:

        if count > self.job_poll_max_count:
            raise RuntimeError(
                f"Export users job incomplete "
                f"(polled {self.job_poll_max_count} time(s) "
                f"at {self.job_poll_interval_ms} ms intervals). "
                f"`job_poll_interval_ms` and `job_poll_max_count` may need adjusting."
            )

        get_job_response = self._request(get_job_request, None)
        job = get_job_response.json()

        if job["status"] == "pending":
            time.sleep(self.job_poll_interval_ms / 1000)
            return self._poll_job(get_job_request, count=count + 1)

        return job


class ClientsStream(Auth0Stream):
    """Define clients stream."""

    name = "clients"
    records_jsonpath = "$.clients[*]"
    path = "/clients"
    primary_keys = ["client_id"]
    schema = ClientObject.schema
