# Copyright (c) 2026 Meltano.

"""Tests standard tap features using the built-in SDK tests library."""

import datetime as dt
import os

import pytest
from singer_sdk.testing import get_tap_test_class

from tap_auth0.tap import TapAuth0

# the test class syncs the live API when it is built
if "TAP_AUTH0_CLIENT_ID" not in os.environ:
    pytest.skip("the standard tap tests need Auth0 credentials", allow_module_level=True)

SAMPLE_CONFIG = {
    "start_date": dt.datetime.now(dt.timezone.utc).date().isoformat(),
}


# Run standard built-in tap tests from the SDK:
TestTapAuth0 = get_tap_test_class(
    tap_class=TapAuth0,
    config=SAMPLE_CONFIG,
)
