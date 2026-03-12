import logging
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import VMCDataUpdateCoordinator
from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensori VMC."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    sensors = [VMCSensor(coordinator, key, cfg) for key, cfg in SENSOR_TYPES.items()]
    async_add_entities(sensors, update_before_add=True)


class VMCSensor(CoordinatorEntity, SensorEntity):
    """Sensore VMC Modbus."""

    def __init__(self, coordinator: VMCDataUpdateCoordinator, key: str, config: dict):
        super().__init__(coordinator)
        self._key = key
        self._config = config
        self._attr_unique_id = f"vmc_{key}"
        self._attr_name = config["name"]
        self._attr_icon = config["icon"]

        if config.get("device_class"):
            self._attr_device_class = config["device_class"]

        if config.get("unit"):
            self._attr_native_unit_of_measurement = config["unit"]
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        """Valore del sensore."""
        if self.coordinator.data is None:
            return None

        if self._key == "modalita_gestione":
            return self.coordinator.data.get(self._key + "_text")

        return self.coordinator.data.get(self._key)

    @property
    def available(self) -> bool:
        """Disponibilità sensore."""
        return self.coordinator.last_update_success and self.coordinator.data is not None
