"""pytest configuration for gsheets tests."""

import pytest


def pytest_configure(config):
    """Configure pytest-asyncio to auto-detect async tests."""
    # Set asyncio mode to auto so async def tests run without explicit marker
    try:
        config.option.asyncio_mode = "auto"
    except Exception:
        pass
