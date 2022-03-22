"""Tests the tap using a mock base credentials config."""

import gzip
import json
import unittest

import ndjson
import responses
import singer

import tap_auth0.tests.utils as test_utils
from tap_auth0.tap import TapAuth0


class TestTapAuth0Sync(unittest.TestCase):
    """Test class for tap-auth0 using base credentials"""

    def setUp(self):
        self.mock_config = {
            "client_id": "1234",
            "client_secret": "1234",
            "domain": "test.auth0.com",
        }
        responses.reset()
        del test_utils.SINGER_MESSAGES[:]

        singer.write_message = test_utils.accumulate_singer_messages

    def test_base_credentials_discovery(self):
        """Test basic discover sync"""

        catalog = TapAuth0(self.mock_config).discover_streams()

        # expect valid catalog to be discovered
        self.assertEqual(len(catalog), 3, "Total streams from default catalog")

    @responses.activate
    def test_auth0_sync_users(self):
        """Test sync users."""

        tap = test_utils.set_up_tap_with_custom_catalog(
            self.mock_config, ["stream_auth0_users"]
        )

        responses.add(
            responses.POST,
            "https://test.auth0.com/oauth/token",
            json={"access_token": "12345", "expires_in": 3622},
            status=200,
        )

        job_id = "12345"
        job = test_utils.users_export_job_pending(job_id)
        responses.add(
            responses.POST,
            "https://test.auth0.com/api/v2/jobs/users-exports",
            status=200,
            json=job,
        )

        job = test_utils.users_export_job_processing(job_id)
        responses.add(
            responses.POST,
            "https://test.auth0.com/api/v2/jobs/users-exports",
            status=200,
            json=job,
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

        tap.sync_all()

        self.assertEqual(len(test_utils.SINGER_MESSAGES), 3)
        self.assertIsInstance(test_utils.SINGER_MESSAGES[0], singer.SchemaMessage)
        self.assertIsInstance(test_utils.SINGER_MESSAGES[1], singer.RecordMessage)
        self.assertIsInstance(test_utils.SINGER_MESSAGES[2], singer.StateMessage)

    @responses.activate
    def test_auth0_sync_users_failed(self):
        """Test sync users with failed job"""

        tap = test_utils.set_up_tap_with_custom_catalog(
            self.mock_config, ["stream_auth0_users"]
        )

        responses.add(
            responses.POST,
            "https://test.auth0.com/oauth/token",
            json={"access_token": "12345", "expires_in": 3622},
            status=200,
        )

        job_id = "12345"
        job = test_utils.users_export_job_pending(job_id)
        responses.add(
            responses.POST,
            "https://test.auth0.com/api/v2/jobs/users-exports",
            status=200,
            json=job,
        )

        job = test_utils.users_export_job_processing(job_id)
        responses.add(
            responses.POST,
            "https://test.auth0.com/api/v2/jobs/users-exports",
            status=200,
            json=job,
        )

        job = test_utils.users_export_job_failed(job_id)
        responses.add(
            responses.GET,
            f"https://test.auth0.com/api/v2/jobs/{job_id}",
            status=200,
            json=job,
        )

        with self.assertRaises(RuntimeError) as err:
            tap.sync_all()

        self.assertIn(f"Job '{job_id}' failed", str(err.exception))

        self.assertEqual(len(test_utils.SINGER_MESSAGES), 1)
        self.assertIsInstance(test_utils.SINGER_MESSAGES[0], singer.SchemaMessage)

    @responses.activate
    def test_auth0_sync_clients(self):
        """Test sync clients."""

        tap = test_utils.set_up_tap_with_custom_catalog(
            self.mock_config, ["stream_auth0_clients"]
        )

        responses.add(
            responses.POST,
            "https://test.auth0.com/oauth/token",
            json={"access_token": "12345", "expires_in": 3622},
            status=200,
        )

        responses.add(
            responses.GET,
            "https://test.auth0.com/api/v2/clients",
            json=test_utils.clients_data,
            status=200,
        )

        tap.sync_all()

        self.assertEqual(len(test_utils.SINGER_MESSAGES), 3)
        self.assertIsInstance(test_utils.SINGER_MESSAGES[0], singer.SchemaMessage)
        self.assertIsInstance(test_utils.SINGER_MESSAGES[1], singer.RecordMessage)
        self.assertIsInstance(test_utils.SINGER_MESSAGES[2], singer.StateMessage)

    @responses.activate
    def test_auth0_sync_logs(self):
        """Test sync logs."""

        tap = test_utils.set_up_tap_with_custom_catalog(
            self.mock_config, ["stream_auth0_logs"]
        )

        responses.add(
            responses.POST,
            "https://test.auth0.com/oauth/token",
            json={"access_token": "12345", "expires_in": 3622},
            status=200,
        )

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

        tap.sync_all()

        self.assertIsInstance(test_utils.SINGER_MESSAGES[0], singer.SchemaMessage)
        self.assertIsInstance(test_utils.SINGER_MESSAGES[1], singer.RecordMessage)
        self.assertIsInstance(test_utils.SINGER_MESSAGES[2], singer.StateMessage)

        # Assert that the log_id is used as the last state
        replication_key_value = test_utils.SINGER_MESSAGES[2].asdict()
        replication_key_value = replication_key_value["value"]["bookmarks"][
            "stream_auth0_logs"
        ]["replication_key_value"]
        self.assertEqual("log_id_12345", replication_key_value)
