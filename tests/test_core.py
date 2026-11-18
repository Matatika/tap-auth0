# Copyright (c) 2026 Meltano.

"""Tests standard tap features using the built-in SDK tests library."""

import datetime as dt

from singer_sdk.testing import get_tap_test_class

from tap_auth0.tap import TapAuth0

SAMPLE_CONFIG = {
    "start_date": dt.datetime.now(dt.timezone.utc).date().isoformat(),
}


# Run standard built-in tap tests from the SDK:
TestTapAuth0 = get_tap_test_class(
    tap_class=TapAuth0,
    config=SAMPLE_CONFIG,
)
