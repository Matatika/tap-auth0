"""Stream type classes for tap-auth0."""

import gzip
import json
import time
from typing import Any, Dict, Iterable, Optional

import ndjson
import requests
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
from singer_sdk.helpers.jsonpath import extract_jsonpath


from tap_auth0.client import Auth0Stream
from tap_auth0.schemas.client import ClientObject
from tap_auth0.schemas.log import LogObject
from tap_auth0.schemas.user import UserObject


class UsersStream(Auth0Stream):
    """Define users stream."""

    name = "stream_auth0_users"
    primary_keys = ["user_id"]
    schema = UserObject.schema
    authenticator = None
    url_base = ""

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
        job_poll_interval_ms = self.config["job_poll_interval_ms"]
        job_poll_max_count = self.config["job_poll_max_count"]

        if count > job_poll_max_count:
            raise RuntimeError(
                f"Export users job incomplete "
                f"(polled {job_poll_max_count} time(s) "
                f"at {job_poll_interval_ms} ms intervals). "
                f"`job_poll_interval_ms` and `job_poll_max_count` may need adjusting."
            )

        get_job_response = self._request(get_job_request, None)
        job = get_job_response.json()

        if job["status"] == "pending":
            time.sleep(job_poll_interval_ms / 1000)
            return self._poll_job(get_job_request, count=count + 1)

        return job


class ClientsStream(Auth0Stream):
    """Define clients stream."""

    name = "stream_auth0_clients"
    records_jsonpath = "$.clients[*]"
    path = "/clients"
    primary_keys = ["client_id"]
    schema = ClientObject.schema


class LogsStream(Auth0Stream):
    """Define logs stream."""

    name = "stream_auth0_logs"
    path = "/logs"
    primary_keys = ["log_id"]
    schema = LogObject.schema
    log_expired = False

    replication_key = "log_id"

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        params = {}
        params["sort"] = "date:1"
        self.per_page = 1
        params["per_page"] = self.per_page

        if self.log_expired:
            self.log_expired = False
            return params

        if next_page_token or self.get_context_state(context).get(
            "replication_key_value"
        ):

            state = self.get_context_state(context).get("replication_key_value")

            self.per_page = 100

            params["take"] = self.per_page
            params["per_page"] = self.per_page
            params["from"] = next_page_token or state

        return params

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Any:

        if response.status_code == 400:
            self.log_expired = True
            return True

        all_matches = extract_jsonpath(
            f"$[{self.per_page - 1}].log_id", response.json()
        )

        try:
            last_element = next(iter(all_matches))
            return last_element
        except StopIteration:
            return None

    def validate_response(self, response: requests.Response) -> None:

        if response.status_code == 400:
            return

        elif 401 <= response.status_code < 500:
            msg = (
                f"{response.status_code} Client Error: "
                f"{response.reason} for path: {self.path}"
            )
            raise FatalAPIError(msg)

        elif 500 <= response.status_code < 600:
            msg = (
                f"{response.status_code} Server Error: "
                f"{response.reason} for path: {self.path}"
            )
            raise RetriableAPIError(msg)

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        if response.status_code == 400:
            return []
        return super().parse_response(response)
