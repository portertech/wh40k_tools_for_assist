"""Test the WH40k Tools for Assist integration."""

from unittest.mock import MagicMock, patch

import pytest

from custom_components.wh40k_tools_for_assist import (
    DOMAIN,
    async_setup,
    async_setup_entry,
    async_unload_entry,
)


class TestWh40kToolsIntegration:
    """Test the WH40k Tools for Assist integration setup and teardown."""

    @pytest.mark.asyncio
    async def test_async_setup(self, mock_hass: MagicMock) -> None:
        """Test the async_setup function."""
        result = await async_setup(mock_hass, {})

        assert result is True
        assert DOMAIN in mock_hass.data

    @pytest.mark.asyncio
    async def test_async_setup_entry(
        self, mock_hass: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test setting up a config entry."""
        mock_hass.data[DOMAIN] = {}
        mock_hass.config_entries.async_entries.return_value = [mock_config_entry]

        with patch(
            "custom_components.wh40k_tools_for_assist.setup_llm_functions"
        ) as mock_setup:
            result = await async_setup_entry(mock_hass, mock_config_entry)

            assert result is True
            mock_setup.assert_called_once_with(mock_hass, mock_config_entry.data)

    @pytest.mark.asyncio
    async def test_async_unload_entry(
        self, mock_hass: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test unloading a config entry."""
        mock_hass.data[DOMAIN] = {
            "api": MagicMock(),
            "config": mock_config_entry.data,
            "unregister_api": MagicMock(),
        }

        with patch(
            "custom_components.wh40k_tools_for_assist.cleanup_llm_functions"
        ) as mock_cleanup:
            result = await async_unload_entry(mock_hass, mock_config_entry)

            assert result is True
            mock_cleanup.assert_called_once_with(mock_hass)
