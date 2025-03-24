"""Stream type classes for tap-auth0."""

from __future__ import annotations

import gzip
import json
import time
from http import HTTPStatus
from typing import TYPE_CHECKING

import ndjson
from singer_sdk.helpers.jsonpath import extract_jsonpath
from typing_extensions import override

from tap_auth0.client import Auth0Stream
from tap_auth0.pagination import LogsPaginator
from tap_auth0.schemas.client import ClientObject
from tap_auth0.schemas.log import LogObject
from tap_auth0.schemas.user import UserObject

if TYPE_CHECKING:
    import requests


class UsersStream(Auth0Stream):
    """Define users stream."""

    name = "stream_auth0_users"
    primary_keys = ("user_id",)
    schema = UserObject.to_dict()
    url_base = ""

    # since Auth0 restricts the total number of users returned from the get users
    # endpoint to 1000 (including paging), we need to create a user export job in order
    # to bypass this limitation
    #
    # https://auth0.com/docs/manage-users/user-search/retrieve-users-with-get-users-endpoint#limitations
    @override
    def get_records(self, context):
        url_base = super().url_base

        # create export users job
        # https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
        self.path = "/jobs/users-exports"
        create_export_users_job_request = self.build_prepared_request(
            "POST",
            url_base + self.path,
            json={
                "format": "json",
                "fields": [{"name": name} for name in self.schema["properties"]],
            },
        )

        export_users_job = self._request(create_export_users_job_request, None)
        job_id = export_users_job.json()["id"]

        # poll export users job
        # https://auth0.com/docs/api/management/v2#!/Jobs/get_jobs_by_id
        self.path = f"/jobs/{job_id}"
        get_export_users_job_request = self.build_prepared_request(
            "GET",
            url_base + self.path,
        )

        export_users_job = self._poll_job(get_export_users_job_request)
        self.path = export_users_job["location"]
        self.authenticator = None

        return super().get_records(context)

    @override
    def parse_response(self, response):
        users = gzip.decompress(response.content)
        users_ndjson = json.loads(users, cls=ndjson.Decoder)

        yield from extract_jsonpath(self.records_jsonpath, users_ndjson)

    def _poll_job(self, get_job_request: requests.PreparedRequest, count=1):
        job_poll_interval_ms = self.config["job_poll_interval_ms"]
        job_poll_max_count = self.config["job_poll_max_count"]

        if count > job_poll_max_count:
            msg = (
                f"Export users job incomplete (polled {job_poll_max_count} time(s) at "
                f"{job_poll_interval_ms} ms intervals). `job_poll_interval_ms` and "
                "`job_poll_max_count` may need adjusting."
            )
            raise RuntimeError(msg)

        get_job_response = self._request(get_job_request, None)
        job = get_job_response.json()

        status = job["status"]

        if status == "completed":
            return job

        if status == "failed":
            id_ = job["id"]
            summary: dict[str, int] = job["summary"]
            summary_format = ", ".join(f"{k}: {v}" for k, v in summary.items())

            msg = f"Job '{id_}' failed ({summary_format})"
            raise RuntimeError(msg)

        time.sleep(job_poll_interval_ms / 1000)
        return self._poll_job(get_job_request, count=count + 1)


class ClientsStream(Auth0Stream):
    """Define clients stream."""

    name = "stream_auth0_clients"
    path = "/clients"
    primary_keys = ("client_id",)
    schema = ClientObject.to_dict()


class LogsStream(Auth0Stream):
    """Define logs stream."""

    name = "stream_auth0_logs"
    path = "/logs"
    primary_keys = ("log_id",)
    replication_key = "log_id"
    schema = LogObject.to_dict()
    log_expired = False

    @override
    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)

        if params:
            return params

        context_state = self.get_context_state(context)
        last_log_id = next_page_token or context_state.get("replication_key_value")
        log_expired = last_log_id is True

        if last_log_id and not log_expired:
            params["from"] = last_log_id
            params["take"] = 100

        else:
            params["sort"] = "date:1"
            params["per_page"] = 1

        return params

    @override
    def get_new_paginator(self):
        return LogsPaginator()

    @override
    def validate_response(self, response):
        if response.status_code == HTTPStatus.BAD_REQUEST:
            return

        super().validate_response(response)

    @override
    def parse_response(self, response):
        if response.status_code == HTTPStatus.BAD_REQUEST:
            return []

        return super().parse_response(response)

    @override
    def post_process(self, row, context=None):
        row = super().post_process(row, context)
        if isinstance(scope := row.get("scope"), str):
            row.update({"scope": scope.split()})
        return row
