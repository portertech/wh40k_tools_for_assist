"""Test the WH40k Tools for Assist config flow."""

from unittest.mock import MagicMock

import pytest

from custom_components.wh40k_tools_for_assist.config_flow import (
    STEP_USER,
    STEP_WH40K_FANDOM,
    STEP_WH40K_LEXICANUM,
    STEP_WH40K_WAHAPEDIA,
    Wh40kToolsConfigFlow,
    get_next_step,
)
from custom_components.wh40k_tools_for_assist.const import (
    CONF_WH40K_FANDOM_ENABLED,
    CONF_WH40K_LEXICANUM_ENABLED,
    CONF_WH40K_WAHAPEDIA_ENABLED,
)


class TestGetNextStep:
    """Test the get_next_step helper function."""

    def test_no_services_selected(self) -> None:
        """Test when no services are selected."""
        config_data = {
            CONF_WH40K_LEXICANUM_ENABLED: False,
            CONF_WH40K_FANDOM_ENABLED: False,
            CONF_WH40K_WAHAPEDIA_ENABLED: False,
        }
        result = get_next_step(STEP_USER, config_data)
        assert result is None

    def test_lexicanum_selected(self) -> None:
        """Test when only Lexicanum is selected."""
        config_data = {
            CONF_WH40K_LEXICANUM_ENABLED: True,
            CONF_WH40K_FANDOM_ENABLED: False,
            CONF_WH40K_WAHAPEDIA_ENABLED: False,
        }
        result = get_next_step(STEP_USER, config_data)
        assert result is not None
        assert result[0] == STEP_WH40K_LEXICANUM

    def test_fandom_selected_after_lexicanum(self) -> None:
        """Test progression from Lexicanum to Fandom step."""
        config_data = {
            CONF_WH40K_LEXICANUM_ENABLED: True,
            CONF_WH40K_FANDOM_ENABLED: True,
            CONF_WH40K_WAHAPEDIA_ENABLED: False,
        }
        result = get_next_step(STEP_WH40K_LEXICANUM, config_data)
        assert result is not None
        assert result[0] == STEP_WH40K_FANDOM

    def test_wahapedia_selected_after_fandom(self) -> None:
        """Test progression from Fandom to Wahapedia step."""
        config_data = {
            CONF_WH40K_LEXICANUM_ENABLED: True,
            CONF_WH40K_FANDOM_ENABLED: True,
            CONF_WH40K_WAHAPEDIA_ENABLED: True,
        }
        result = get_next_step(STEP_WH40K_FANDOM, config_data)
        assert result is not None
        assert result[0] == STEP_WH40K_WAHAPEDIA

    def test_no_more_steps_after_wahapedia(self) -> None:
        """Test no more steps after Wahapedia."""
        config_data = {
            CONF_WH40K_LEXICANUM_ENABLED: True,
            CONF_WH40K_FANDOM_ENABLED: True,
            CONF_WH40K_WAHAPEDIA_ENABLED: True,
        }
        result = get_next_step(STEP_WH40K_WAHAPEDIA, config_data)
        assert result is None


class TestWh40kToolsConfigFlow:
    """Test the config flow."""

    @pytest.fixture
    def config_flow(self, mock_hass: MagicMock) -> Wh40kToolsConfigFlow:
        """Create a config flow instance."""
        flow = Wh40kToolsConfigFlow()
        flow.hass = mock_hass
        return flow

    @pytest.mark.asyncio
    async def test_step_user_no_entries(
        self, config_flow: Wh40kToolsConfigFlow
    ) -> None:
        """Test initial user step with no existing entries."""
        config_flow._async_current_entries = MagicMock(return_value=[])  # noqa: SLF001

        result = await config_flow.async_step_user(user_input=None)

        assert result["type"] == "form"
        assert result["step_id"] == STEP_USER

    @pytest.mark.asyncio
    async def test_step_user_existing_entry(
        self, config_flow: Wh40kToolsConfigFlow, mock_config_entry: MagicMock
    ) -> None:
        """Test user step aborts when entry exists."""
        config_flow._async_current_entries = MagicMock(  # noqa: SLF001
            return_value=[mock_config_entry]
        )

        result = await config_flow.async_step_user(user_input=None)

        assert result["type"] == "abort"
        assert result["reason"] == "single_instance_allowed"

    @pytest.mark.asyncio
    async def test_step_user_selects_lexicanum(
        self, config_flow: Wh40kToolsConfigFlow
    ) -> None:
        """Test user selecting Lexicanum proceeds to Lexicanum config."""
        config_flow._async_current_entries = MagicMock(return_value=[])  # noqa: SLF001
        config_flow.async_set_unique_id = MagicMock()
        config_flow._abort_if_unique_id_configured = MagicMock()  # noqa: SLF001

        user_input = {
            CONF_WH40K_LEXICANUM_ENABLED: True,
            CONF_WH40K_FANDOM_ENABLED: False,
            CONF_WH40K_WAHAPEDIA_ENABLED: False,
        }

        result = await config_flow.async_step_user(user_input=user_input)

        assert result["type"] == "form"
        assert result["step_id"] == STEP_WH40K_LEXICANUM

    @pytest.mark.asyncio
    async def test_step_user_no_services_creates_entry(
        self, config_flow: Wh40kToolsConfigFlow
    ) -> None:
        """Test user selecting no services creates entry immediately."""
        config_flow._async_current_entries = MagicMock(return_value=[])  # noqa: SLF001
        config_flow.async_set_unique_id = MagicMock()
        config_flow._abort_if_unique_id_configured = MagicMock()  # noqa: SLF001
        config_flow.async_create_entry = MagicMock(
            return_value={"type": "create_entry"}
        )

        user_input = {
            CONF_WH40K_LEXICANUM_ENABLED: False,
            CONF_WH40K_FANDOM_ENABLED: False,
            CONF_WH40K_WAHAPEDIA_ENABLED: False,
        }

        result = await config_flow.async_step_user(user_input=user_input)

        assert result["type"] == "create_entry"
