"""WH40k Tools for Assist integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import ADDON_NAME, DOMAIN
from .llm_functions import cleanup_llm_functions, setup_llm_functions

__all__ = ["DOMAIN"]

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the WH40k Tools for Assist integration."""
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.info("Setting up %s integration", ADDON_NAME)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WH40k Tools for Assist from a config entry."""
    _LOGGER.info("Setting up %s for entry: %s", ADDON_NAME, entry.entry_id)
    await setup_llm_functions(hass, entry.data)
    _LOGGER.info("%s functions successfully set up", ADDON_NAME)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading %s for entry: %s", ADDON_NAME, entry.entry_id)
    await cleanup_llm_functions(hass)
    _LOGGER.info("%s functions successfully unloaded", ADDON_NAME)
    return True
