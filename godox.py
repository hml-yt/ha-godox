import asyncio
from bleak.backends.device import BLEDevice
from bleak import BleakClient
from crccheck.crc import Crc8Maxim
import logging

WRITE_UUID = "0000fec7-0000-1000-8000-00805f9b34fb"
LOGGER = logging.getLogger(__name__)

class GodoxInstance:
    def __init__(self, ble_device: BLEDevice) -> None:
        self._ble_device = ble_device
        self._is_on = None
        self._connected = None
        self._brightness = None

    async def _send(self, data: bytearray):
        LOGGER.debug(''.join(format(x, ' 03x') for x in data))
        
        if (not self._connected):
            await self.connect()
        
        crcinst = Crc8Maxim()
        crcinst.process(data)
        await self._device.write_gatt_char(WRITE_UUID, data + crcinst.finalbytes())

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    async def set_brightness(self, intensity: int):
        header = bytes.fromhex("f0d10501")
        command = bytes([intensity])
        params = bytes.fromhex("380c01")

        await self._send(header + command + params)

        self._brightness = intensity

    async def turn_on(self):
        header = bytes.fromhex("f0d0060c")
        command = bytes.fromhex("01")
        params = bytes.fromhex("00000000")

        await self._send(header + command + params)
        self._is_on = True

    async def turn_off(self):
        header = bytes.fromhex("f0d0060c")
        command = bytes.fromhex("00")
        params = bytes.fromhex("00000000")

        await self._send(header + command + params)
        self._is_on = False

    async def connect(self):
        self._device = BleakClient(self._ble_device)
        await self._device.connect(timeout=20)
        await asyncio.sleep(1)
        self._connected = True

    async def disconnect(self):
        if self._device.is_connected:
            await self._device.disconnect()