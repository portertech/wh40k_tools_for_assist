"""Test configuration for WH40k Tools for Assist integration."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.wh40k_tools_for_assist.const import (
    CONF_WH40K_FANDOM_ENABLED,
    CONF_WH40K_FANDOM_NUM_RESULTS,
    CONF_WH40K_LEXICANUM_ENABLED,
    CONF_WH40K_LEXICANUM_NUM_RESULTS,
    CONF_WH40K_WAHAPEDIA_ENABLED,
    CONF_WH40K_WAHAPEDIA_NUM_RESULTS,
    DOMAIN,
)


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock HomeAssistant instance."""
    hass = MagicMock(spec=HomeAssistant)
    hass.data = {}
    hass.config_entries = MagicMock()
    hass.async_create_task = AsyncMock()
    return hass


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Create a mock ConfigEntry with all tools enabled."""
    entry = MagicMock(spec=ConfigEntry)
    entry.domain = DOMAIN
    entry.entry_id = "test_entry"
    entry.data = {
        CONF_WH40K_LEXICANUM_ENABLED: True,
        CONF_WH40K_LEXICANUM_NUM_RESULTS: 1,
        CONF_WH40K_FANDOM_ENABLED: True,
        CONF_WH40K_FANDOM_NUM_RESULTS: 1,
        CONF_WH40K_WAHAPEDIA_ENABLED: True,
        CONF_WH40K_WAHAPEDIA_NUM_RESULTS: 3,
    }
    entry.options = {}
    return entry


@pytest.fixture
def mock_config_entry_lexicanum_only() -> MagicMock:
    """Create a mock ConfigEntry with only Lexicanum enabled."""
    entry = MagicMock(spec=ConfigEntry)
    entry.domain = DOMAIN
    entry.entry_id = "test_lexicanum_entry"
    entry.data = {
        CONF_WH40K_LEXICANUM_ENABLED: True,
        CONF_WH40K_LEXICANUM_NUM_RESULTS: 2,
        CONF_WH40K_FANDOM_ENABLED: False,
        CONF_WH40K_WAHAPEDIA_ENABLED: False,
    }
    entry.options = {}
    return entry


@pytest.fixture
def lexicanum_search_results() -> dict[str, Any]:
    """Sample Lexicanum search results."""
    return {
        "query": {
            "search": [
                {"title": "Space Marines", "snippet": "The Space Marines are..."},
                {"title": "Ultramarines", "snippet": "The Ultramarines are..."},
            ]
        }
    }


@pytest.fixture
def fandom_search_results() -> dict[str, Any]:
    """Sample Fandom search results."""
    return {
        "query": {
            "search": [
                {"title": "Horus Heresy", "snippet": "The Horus Heresy was..."},
                {"title": "Emperor of Mankind", "snippet": "The Emperor is..."},
            ]
        }
    }


@pytest.fixture
def wahapedia_html_content() -> str:
    """Sample Wahapedia HTML content."""
    return """
    <html>
    <body>
        <h2>Shooting Phase</h2>
        <p>In the Shooting phase, units can fire their ranged weapons.</p>
        <h2>Charge Phase</h2>
        <p>In the Charge phase, units can attempt to charge enemy units.</p>
    </body>
    </html>
    """
