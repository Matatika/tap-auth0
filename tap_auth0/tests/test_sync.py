# Copyright (c) 2026 Meltano.

"""Tests the tap sync using a mock base credentials config."""

import contextlib
import gzip
import io
import json

import ndjson
import pytest
import responses

import tap_auth0.tests.utils as test_utils


def _add_token_response():
    responses.add(
        responses.POST,
        "https://test.auth0.com/oauth/token",
        json={"access_token": "12345", "expires_in": 3622},
        status=200,
    )


def _capture_singer_messages(tap):
    captured_stdout = io.StringIO()
    with contextlib.redirect_stdout(captured_stdout):
        tap.sync_all()

    return [json.loads(line) for line in captured_stdout.getvalue().splitlines()]


@responses.activate
def test_auth0_sync_users():
    """Test sync users."""
    tap = test_utils.set_up_tap_with_custom_catalog(
        test_utils.MOCK_CONFIG, ["stream_auth0_users"]
    )

    _add_token_response()

    job_id = "12345"
    responses.add(
        responses.POST,
        "https://test.auth0.com/api/v2/jobs/users-exports",
        status=200,
        json=test_utils.users_export_job_pending(job_id),
    )
    responses.add(
        responses.POST,
        "https://test.auth0.com/api/v2/jobs/users-exports",
        status=200,
        json=test_utils.users_export_job_processing(job_id),
    )

    job = test_utils.users_export_job_completed(job_id)
    responses.add(
        responses.GET,
        f"https://test.auth0.com/api/v2/jobs/{job_id}",
        status=200,
        json=job,
    )
    responses.add(
        responses.GET,
        job["location"],
        status=200,
        body=gzip.compress(
            json.dumps(test_utils.users_data, cls=ndjson.Encoder).encode()
        ),
    )

    singer_messages = _capture_singer_messages(tap)

    assert [message["type"] for message in singer_messages] == [
        "SCHEMA",
        "RECORD",
        "STATE",
    ]
    assert singer_messages[1]["record"] == {"user_id": "user_id_12345"}


@responses.activate
def test_auth0_sync_users_failed():
    """Test sync users with a failed job."""
    tap = test_utils.set_up_tap_with_custom_catalog(
        test_utils.MOCK_CONFIG, ["stream_auth0_users"]
    )

    _add_token_response()

    job_id = "12345"
    responses.add(
        responses.POST,
        "https://test.auth0.com/api/v2/jobs/users-exports",
        status=200,
        json=test_utils.users_export_job_pending(job_id),
    )
    responses.add(
        responses.POST,
        "https://test.auth0.com/api/v2/jobs/users-exports",
        status=200,
        json=test_utils.users_export_job_processing(job_id),
    )
    responses.add(
        responses.GET,
        f"https://test.auth0.com/api/v2/jobs/{job_id}",
        status=200,
        json=test_utils.users_export_job_failed(job_id),
    )

    captured_stdout = io.StringIO()
    with (
        contextlib.redirect_stdout(captured_stdout),
        pytest.raises(RuntimeError, match=f"Job '{job_id}' failed"),
    ):
        tap.sync_all()

    singer_messages = [
        json.loads(line) for line in captured_stdout.getvalue().splitlines()
    ]

    assert [message["type"] for message in singer_messages] == ["SCHEMA"]


@responses.activate
def test_auth0_sync_clients():
    """Test sync clients."""
    tap = test_utils.set_up_tap_with_custom_catalog(
        test_utils.MOCK_CONFIG, ["stream_auth0_clients"]
    )

    _add_token_response()

    responses.add(
        responses.GET,
        "https://test.auth0.com/api/v2/clients",
        json=test_utils.clients_data,
        status=200,
    )

    singer_messages = _capture_singer_messages(tap)

    assert [message["type"] for message in singer_messages] == [
        "SCHEMA",
        "RECORD",
        "STATE",
    ]


@responses.activate
def test_auth0_sync_logs():
    """Test sync logs."""
    tap = test_utils.set_up_tap_with_custom_catalog(
        test_utils.MOCK_CONFIG, ["stream_auth0_logs"]
    )

    _add_token_response()

    responses.add(
        responses.GET,
        "https://test.auth0.com/api/v2/logs",
        json=test_utils.logs_data,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://test.auth0.com/api/v2/logs",
        json=[],
        status=200,
    )

    singer_messages = _capture_singer_messages(tap)

    assert [message["type"] for message in singer_messages] == [
        "SCHEMA",
        "RECORD",
        "STATE",
    ]
    assert singer_messages[1]["record"] == {"log_id": "log_id_12345"}

    # the log_id is used as the last state
    bookmark = singer_messages[2]["value"]["bookmarks"]["stream_auth0_logs"]
    assert bookmark["replication_key_value"] == "log_id_12345"
