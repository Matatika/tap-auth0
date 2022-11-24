"""Stream type classes for tap-auth0."""

import gzip
import json
import time
from typing import Any, Dict, Iterable, Optional

import ndjson
import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath

from tap_auth0.client import Auth0Stream
from tap_auth0.pagination import LogsPaginator
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

        status = job["status"]

        if status == "completed":
            return job

        if status == "failed":
            id_ = job["id"]
            summary: dict[str, int] = job["summary"]
            summary_format = ", ".join(f"{k}: {v}" for k, v in summary.items())

            raise RuntimeError(f"Job '{id_}' failed ({summary_format})")

        time.sleep(job_poll_interval_ms / 1000)
        return self._poll_job(get_job_request, count=count + 1)


class ClientsStream(Auth0Stream):
    """Define clients stream."""

    name = "stream_auth0_clients"
    path = "/clients"
    primary_keys = ["client_id"]
    schema = ClientObject.schema


class LogsStream(Auth0Stream):
    """Define logs stream."""

    name = "stream_auth0_logs"
    path = "/logs"
    primary_keys = ["log_id"]
    replication_key = "log_id"
    schema = LogObject.schema
    log_expired = False

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)

        if params:
            return params

        context_state = self.get_context_state(context)
        last_log_id = next_page_token or context_state.get("replication_key_value")

        if last_log_id and not self.log_expired:
            params["from"] = last_log_id
            params["take"] = 100

        else:
            params["sort"] = "date:1"
            params["per_page"] = 1

        return params

    def get_new_paginator(self):
        def log_expired_callback(response: requests.Response):
            self.log_expired = response.status_code == 400
            return self.log_expired

        return LogsPaginator(log_expired_callback)

    def validate_response(self, response: requests.Response):
        if response.status_code == 400:
            return

        super().validate_response(response)
        self.log_expired = False

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        return [] if response.status_code == 400 else super().parse_response(response)

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        row = super().post_process(row, context)
        scope = row.get("scope")
        if isinstance(scope, str):
            row.update({"scope": scope.split()})
        return row
