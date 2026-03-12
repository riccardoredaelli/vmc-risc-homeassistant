import logging
from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from pymodbus.client import AsyncModbusTcpClient
from .coordinator import VMCDataUpdateCoordinator
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_SLAVE_ID, VELOCITA_MAP

_LOGGER = logging.getLogger(__name__)

SPEED_PERCENTAGES = {0: 0, 1: 20, 2: 40, 3: 60, 4: 80, 5: 100}
PERCENTAGE_TO_SPEED = {v: k for k, v in SPEED_PERCENTAGES.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([VMCFan(coordinator, config_entry.data)], update_before_add=True)


class VMCFan(CoordinatorEntity, FanEntity):

    _attr_name = "VMC Casa"
    _attr_unique_id = "vmc_fan_principale"
    _attr_supported_features = FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE
    _attr_preset_modes = list(VELOCITA_MAP.values())

    def __init__(self, coordinator: VMCDataUpdateCoordinator, config: dict):
        super().__init__(coordinator)
        self._config = config


    async def _write_register(self, address: int, value: int):
        client = AsyncModbusTcpClient(
            host=self._config[CONF_HOST],
            port=self._config[CONF_PORT],
            timeout=3,
        )
        try:
            await client.connect()
            await client.write_register(
                address=address,
                value=value,
                device_id=self._config[CONF_SLAVE_ID]
            )
        finally:
            client.close()
        await self.coordinator.async_request_refresh()


    @property
    def is_on(self) -> bool:
        if self.coordinator.data is None:
            return False
        return self.coordinator.data.get("velocita_selezionata", 0) > 0

    @property
    def percentage(self) -> int:
        if self.coordinator.data is None:
            return 0
        val = self.coordinator.data.get("velocita_selezionata", 0)
        return SPEED_PERCENTAGES.get(val, 0)

    @property
    def preset_mode(self) -> str:
        if self.coordinator.data is None:
            return "OFF"
        val = self.coordinator.data.get("velocita_selezionata", 0)
        return VELOCITA_MAP.get(val, "OFF")

    async def async_turn_on(self, percentage=None, preset_mode=None, **kwargs):
        if preset_mode and preset_mode in VELOCITA_MAP.values():
            val = next(k for k, v in VELOCITA_MAP.items() if v == preset_mode)
        elif percentage is not None:
            val = PERCENTAGE_TO_SPEED.get(percentage, 1)
        else:
            val = 1
        await self._write_register(0, val)

    async def async_turn_off(self, **kwargs):
        await self._write_register(0, 0)

    async def async_set_percentage(self, percentage: int):
        val = PERCENTAGE_TO_SPEED.get(percentage, 1)
        await self._write_register(0, val)

    async def async_set_preset_mode(self, preset_mode: str):
        val = next((k for k, v in VELOCITA_MAP.items() if v == preset_mode), 0)
        await self._write_register(0, val)
