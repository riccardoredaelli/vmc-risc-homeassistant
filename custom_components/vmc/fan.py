from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .coordinator import VMCDataUpdateCoordinator
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([VMCFan(coordinator)])

class VMCFan(FanEntity):
    _attr_name = "VMC Casa"
    _attr_unique_id = "vmc_fan"
    _attr_supported_features = FanEntityFeature.SET_SPEED

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._speed = None

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.get("velocita_attiva", 0) > 0

    @property
    def speed(self):
        return self.coordinator.data.get("velocita_selezionata")

    async def async_turn_on(self, **kwargs):
        # Scrivi register 0 con speed
        pass  # Implementa write

    async def async_turn_off(self, **kwargs):
        pass  # Write 0
