"""Auth0 entry point.

Copyright (c) 2026 Meltano.
"""

from __future__ import annotations

from tap_auth0.tap import TapAuth0

TapAuth0.cli()
