# Copyright (c) 2026 Meltano.

"""Tests the users stream against a mocked Auth0 API."""

import gzip
import json
import time

import pytest
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


@responses.activate
def test_users_job_poll_waits_for_time_left_seconds():
    """A processing job is polled again after its `time_left_seconds`."""
    job_url = "https://test.auth0.com/api/v2/jobs/job_1"
    responses.post(
        "https://test.auth0.com/oauth/token",
        json={"access_token": "token", "expires_in": 3600},
    )
    responses.post(
        "https://test.auth0.com/api/v2/jobs/users-exports",
        json={"id": "job_1", "status": "pending"},
    )
    responses.get(
        job_url,
        json={"id": "job_1", "status": "processing", "time_left_seconds": 1},
    )
    responses.get(
        job_url,
        json={"id": "job_1", "status": "completed", "location": "https://test.com"},
    )
    responses.get("https://test.com", body=gzip.compress(b"{}"))

    start = time.monotonic()
    TapAuth0(config=CONFIG).streams["stream_auth0_users"].sync()

    assert time.monotonic() - start >= 1


@responses.activate
def test_users_job_poll_stops_at_max_count():
    """A job that stays `processing` fails after `job_poll_max_count` polls."""
    job_url = "https://test.auth0.com/api/v2/jobs/job_1"
    responses.post(
        "https://test.auth0.com/oauth/token",
        json={"access_token": "token", "expires_in": 3600},
    )
    responses.post(
        "https://test.auth0.com/api/v2/jobs/users-exports",
        json={"id": "job_1", "status": "pending"},
    )
    poll = responses.get(job_url, json={"id": "job_1", "status": "processing"})

    with pytest.raises(RuntimeError, match="Export users job incomplete"):
        TapAuth0(config=CONFIG | {"job_poll_max_count": 2}).streams["stream_auth0_users"].sync()

    assert poll.call_count == 2
