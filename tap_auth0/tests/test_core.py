# Copyright (c) 2026 Meltano.

"""Tests standard tap features using the built-in SDK tests library."""

import gzip
import json

import ndjson
import pytest
import responses
from singer_sdk.testing import get_tap_test_class

import tap_auth0.tests.utils as test_utils
from tap_auth0.tap import TapAuth0


@pytest.fixture(scope="class", autouse=True)
def _mock_auth0_api():
    """Mock the Auth0 API for the standard tap tests."""
    job_id = "12345"
    job = test_utils.users_export_job_completed(job_id)

    with responses.RequestsMock(assert_all_requests_are_fired=False) as mock:
        mock.add(
            responses.POST,
            "https://test.auth0.com/oauth/token",
            json={"access_token": "12345", "expires_in": 3622},
        )
        mock.add(
            responses.POST,
            "https://test.auth0.com/api/v2/jobs/users-exports",
            json=test_utils.users_export_job_pending(job_id),
        )
        mock.add(
            responses.GET,
            f"https://test.auth0.com/api/v2/jobs/{job_id}",
            json=job,
        )
        mock.add(
            responses.GET,
            job["location"],
            body=gzip.compress(
                json.dumps(test_utils.users_data, cls=ndjson.Encoder).encode()
            ),
        )
        mock.add(
            responses.GET,
            "https://test.auth0.com/api/v2/clients",
            json=test_utils.clients_data,
        )
        mock.add(
            responses.GET,
            "https://test.auth0.com/api/v2/logs",
            json=test_utils.logs_data,
        )
        mock.add(
            responses.GET,
            "https://test.auth0.com/api/v2/logs",
            json=[],
        )
        yield


# Run standard built-in tap tests from the SDK:
TestTapAuth0 = get_tap_test_class(
    tap_class=TapAuth0,
    config=test_utils.MOCK_CONFIG,
)
