import logging
import struct
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from homeassistant.components.modbus import get_hub
from .const import CONF_HOST, CONF_PORT, CONF_SLAVE_ID, SENSOR_TYPES, MODALITA_MAP

_LOGGER = logging.getLogger(__name__)


class VMCDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, config: dict):
        super().__init__(
            hass,
            _LOGGER,
            name="VMC Modbus",
            update_interval=timedelta(seconds=10),
        )
        self.config = config
        self._raw_data = {}

    async def async_shutdown(self):
        pass

    async def _async_update_data(self) -> dict:
        slave = self.config[CONF_SLAVE_ID]
        data = {}

        try:
            hub = get_hub(self.hass, "vmc_waveshare_rs485")
        except Exception:
            hub = None

        if hub is None:
            raise UpdateFailed("Hub Modbus non trovato. Configura modbus in packages/vmc.yaml")

        try:
            for key, cfg in SENSOR_TYPES.items():
                address = cfg["address"]
                dtype = cfg["data_type"]
                count = 2 if dtype == "float32" else 1

                result = await hub.async_pb_call(
                    slave, address, count, "holding"
                )

                if result is None or result.isError():
                    data[key] = None
                    continue

                if dtype == "float32":
                    raw = (result.registers[0] << 16) | result.registers[1]
                    value = struct.unpack(">f", struct.pack(">I", raw))[0]
                    data[key] = round(value, 1)
                else:
                    data[key] = result.registers[0]

                if key == "modalita_gestione":
                    data[key + "_text"] = MODALITA_MAP.get(
                        data[key], f"Sconosciuto {data[key]}"
                    )

            self._raw_data = data
            return data

        except Exception as err:
            _LOGGER.error("Errore lettura VMC: %s", err)
            raise UpdateFailed(f"Errore: {err}") from err
    async def async_write_register(self, address: int, value: int) -> None:
        """Scrivi un registro Modbus."""
        from homeassistant.components.modbus import get_hub
        slave = self.config[CONF_SLAVE_ID]
        try:
            hub = get_hub(self.hass, "vmc_waveshare_rs485")
            await hub.async_pb_call(slave, address, value, "write_register")
            _LOGGER.info("Scritto registro %s = %s", address, value)
        except Exception as err:
            _LOGGER.error("Errore scrittura registro %s: %s", address, err)

