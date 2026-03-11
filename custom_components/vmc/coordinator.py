"""Data coordinator."""
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.components.modbus import hub
from homeassistant.core import HomeAssistant
from .const import CONF_HOST, CONF_PORT, CONF_SLAVE_ID, SENSOR_TYPES, MODALITA_MAP

_LOGGER = logging.getLogger(__name__)

class VMCDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config: dict):
        super().__init__(
            hass,
            _LOGGER,
            name="VMC Modbus",
            update_interval=timedelta(seconds=10)
        )
        self.config = config
        self.hub = None
        self._raw_data = {}

    async def _async_update_data(self):
        try:
            if not self.hub:
                self.hub = hub.get_hub(
                    self.hass,
                    "tcp",
                    host=self.config[CONF_HOST],
                    port=self.config[CONF_PORT]
                )
            
            data = {}
            for key, config in SENSOR_TYPES.items():
                value = await self.hub.async_read_holding_registers(
                    address=config["address"],
                    count=1,
                    slave=self.config[CONF_SLAVE_ID]
                )
                data[key] = value[0] if value else None
                
                if key == "modalita_gestione":
                    data[key + "_text"] = MODALITA_MAP.get(value[0], f"Sconosciuto {value[0]}")
            
            self._raw_data = data
            return data
        except Exception as err:
            _LOGGER.error("Errore lettura Modbus: %s", err)
            return self._raw_data
