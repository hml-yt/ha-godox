from __future__ import annotations

from typing import Any

import logging

from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class GodoxConfigFlow(ConfigFlow, domain=DOMAIN):
    """Godox Config Flow"""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_device: DeviceData | None = None
        self._discovered_devices: dict[str, str] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        _LOGGER.info("Config Flow Started")
        """Handle the bluetooth discovery step."""

        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()

        #device = DeviceData()
        #if not device.supported(discovery_info):
        #    return self.async_abort(reason="not_supported")
        #self._discovered_device = device

        self._discovery_info = discovery_info

        _LOGGER.info(
            "Discovered device %s at address %s",
            discovery_info.name,
            discovery_info.address
        )
        
        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        discovery_info = self._discovery_info
        #title = device.title or device.get_device_name() or discovery_info.name
        title = discovery_info.name
        if user_input is not None:
            return self.async_create_entry(
                title=title,
                data={
                    CONF_ADDRESS: discovery_info.address
                }
            )

        self._set_confirm_only()
        placeholders = {"name": title}
        self.context["title_placeholders"] = placeholders
        return self.async_show_form(
            step_id="bluetooth_confirm", description_placeholders=placeholders
        )
