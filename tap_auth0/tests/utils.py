# Copyright (c) 2026 Meltano.

"""Test utilities."""

from singer_sdk.helpers import _catalog
from singer_sdk.singerlib.catalog import Catalog

from tap_auth0.tap import TapAuth0

MOCK_CONFIG = {
    "client_id": "1234",
    "client_secret": "1234",
    "domain": "test.auth0.com",
}

users_data = [{"user_id": "user_id_12345"}]

clients_data = [{"client_id": "client_id_12345"}]
logs_data = [{"log_id": "log_id_12345"}]


def users_export_job_pending(job_id: str):
    """Return a pending users-export job response."""
    return {
        "status": "pending",
        "id": job_id,
    }


def users_export_job_processing(job_id: str):
    """Return a processing users-export job response."""
    return {
        "status": "processing",
        "id": job_id,
    }


def users_export_job_completed(job_id: str):
    """Return a completed users-export job response."""
    return {
        "status": "completed",
        "id": job_id,
        "location": "https://test.com",
    }


def users_export_job_failed(job_id: str):
    """Return a failed users-export job response."""
    return {
        "status": "failed",
        "id": job_id,
        "summary": {
            "failed": len(users_data),
            "updated": 0,
            "inserted": 0,
            "total": len(users_data),
        },
    }


def set_up_tap_with_custom_catalog(mock_config, stream_list):
    """Create an instance of tap-auth0 with specific config and streams."""
    tap = TapAuth0(config=mock_config)
    # Run discovery
    tap.run_discovery()
    # Get catalog from tap
    catalog = Catalog.from_dict(tap.catalog_dict)
    # Reset and re-initialize with an input catalog
    _catalog.deselect_all_streams(catalog=catalog)
    for stream in stream_list:
        _catalog.set_catalog_stream_selected(
            catalog=catalog,
            stream_name=stream,
            selected=True,
        )
    # Initialise tap with new catalog
    return TapAuth0(config=mock_config, catalog=catalog.to_dict())
