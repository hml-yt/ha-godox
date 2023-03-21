"""The Godox Bluetooth BLE integration."""
from __future__ import annotations

import logging

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup a config entry"""
    _LOGGER.info('Async setup entry in main init')
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(
            entry, "light"
        )
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return hass.config_entries.async_forward_entry_unload(entry, "light")