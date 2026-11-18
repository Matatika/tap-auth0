# Copyright (c) 2026 Meltano.

"""Tests the retry of rate-limited requests against a mocked Auth0 API."""

import json
import time

import responses

from tap_auth0.tap import TapAuth0

CONFIG = {
    "client_id": "1234",
    "client_secret": "1234",
    "domain": "test.auth0.com",
}


@responses.activate
def test_rate_limited_request_waits_for_retry_after(capsys):
    """A 429 response is retried after `Retry-After`, not the exponential wait."""
    clients_url = "https://test.auth0.com/api/v2/clients"
    client = {"client_id": "client_1"}
    responses.post(
        "https://test.auth0.com/oauth/token",
        json={"access_token": "token", "expires_in": 3600},
    )
    responses.get(clients_url, status=429, headers={"Retry-After": "0"})
    responses.get(clients_url, json=[client])

    start = time.monotonic()
    TapAuth0(config=CONFIG).streams["stream_auth0_clients"].sync()

    # the exponential backoff waits at least 2 s, and the jitter adds at most 1 s
    assert time.monotonic() - start < 2
    messages = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    records = [m["record"] for m in messages if m["type"] == "RECORD"]
    assert records == [client]
