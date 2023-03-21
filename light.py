"""Platform for light integration."""
from __future__ import annotations

import logging

from .godox import GodoxInstance
from bleak.backends.device import BLEDevice

from pprint import pformat

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (SUPPORT_BRIGHTNESS, ATTR_BRIGHTNESS,
                                            PLATFORM_SCHEMA, LightEntity)
from homeassistant.const import CONF_NAME, CONF_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components import bluetooth

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> bool:
    """Set up a Godox Light device from a config entry."""
    
    # address: str = entry.data[CONF_ADDRESS]
    _LOGGER.info('Async setup entry in platform', pformat(entry))

    ble_device: BLEDevice = bluetooth.async_ble_device_from_address(
        hass, entry.data[CONF_ADDRESS]
    )

    light = {
        "name": entry.title,
        "device": ble_device
    }
    _LOGGER.info('Light is: ', pformat(light))

    async_add_entities([GodoxLight(light)])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True

class GodoxLight(LightEntity):
    """Representation of an Godox Light."""

    def __init__(self, light) -> None:
        """Initialize an GodoxLight."""
        _LOGGER.info(pformat(light))
        self._light = GodoxInstance(light["device"])
        self._name = light["name"]
        self._state = None
        self._brightness = None

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on."""
        
        if ATTR_BRIGHTNESS in kwargs:
            await self._light.set_brightness(kwargs.get(ATTR_BRIGHTNESS, 255))
            
        await self._light.turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        await self._light.turn_off()

    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._light.is_on
        self._brightness = self._light.brightness    