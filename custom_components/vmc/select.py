import logging
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import VMCDataUpdateCoordinator
from .const import DOMAIN, VELOCITA_MAP

_LOGGER = logging.getLogger(__name__)

# Mappa inversa: "Vel1" → 1
VELOCITA_REVERSE = {v: k for k, v in VELOCITA_MAP.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([VMCVelocitaSelect(coordinator, config_entry.data)])


class VMCVelocitaSelect(CoordinatorEntity, SelectEntity):
    """Selettore velocità VMC."""

    _attr_name = "VMC Velocità"
    _attr_unique_id = "vmc_velocita_select"
    _attr_icon = "mdi:fan"
    _attr_options = list(VELOCITA_MAP.values())  # ["OFF","Vel1","Vel2","Vel3","Vauto1","Vauto2"]

    def __init__(self, coordinator: VMCDataUpdateCoordinator, config: dict):
        super().__init__(coordinator)
        self._config = config

    @property
    def current_option(self) -> str:
        """Opzione attuale letta da Modbus."""
        if self.coordinator.data is None:
            return "OFF"
        val = self.coordinator.data.get("velocita_selezionata", 0)
        return VELOCITA_MAP.get(val, "OFF")

    async def async_select_option(self, option: str) -> None:
        """Scrivi valore su Modbus quando utente seleziona."""
        value = VELOCITA_REVERSE.get(option, 0)
        _LOGGER.info("VMC velocità → %s (%s)", option, value)
        await self.coordinator.async_write_register(0, value)
        await self.coordinator.async_request_refresh()
