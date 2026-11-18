# Copyright (c) 2026 Meltano.

"""Tests standard tap features using the built-in SDK tests library."""

import datetime as dt

from singer_sdk.testing import get_standard_tap_tests

from tap_auth0.tap import TapAuth0

SAMPLE_CONFIG = {
    "start_date": dt.datetime.now(dt.timezone.utc).date().isoformat(),
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapAuth0, config=SAMPLE_CONFIG)
    for test in tests:
        test()
