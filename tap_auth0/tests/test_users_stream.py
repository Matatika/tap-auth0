# Copyright (c) 2026 Meltano.

"""Tests the users stream against a mocked Auth0 API."""

import gzip
import json

import responses

from tap_auth0.tap import TapAuth0

CONFIG = {
    "client_id": "1234",
    "client_secret": "1234",
    "domain": "test.auth0.com",
    "job_poll_interval_ms": 0,
}


@responses.activate
def test_users_sync_retries_rate_limited_job_poll(capsys):
    """A 429 response to a job poll is retried and the users still sync."""
    job_url = "https://test.auth0.com/api/v2/jobs/job_1"
    user = {"user_id": "user_1"}
    responses.post(
        "https://test.auth0.com/oauth/token",
        json={"access_token": "token", "expires_in": 3600},
    )
    responses.post(
        "https://test.auth0.com/api/v2/jobs/users-exports",
        json={"id": "job_1", "status": "pending"},
    )
    responses.get(job_url, status=429)
    responses.get(
        job_url,
        json={"id": "job_1", "status": "completed", "location": "https://test.com"},
    )
    responses.get("https://test.com", body=gzip.compress(json.dumps(user).encode()))

    TapAuth0(config=CONFIG).streams["stream_auth0_users"].sync()

    messages = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    records = [m["record"] for m in messages if m["type"] == "RECORD"]
    assert records == [user]
