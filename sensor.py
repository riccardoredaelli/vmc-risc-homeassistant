"""Sensori VMC."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .coordinator import VMCDataUpdateCoordinator
from .const import DOMAIN, SENSOR_TYPES

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    sensors = []
    for key, config in SENSOR_TYPES.items():
        sensors.append(VMCSensor(coordinator, key, config))
    async_add_entities(sensors)

class VMCSensor(SensorEntity):
    def __init__(self, coordinator: VMCDataUpdateCoordinator, key: str, config: dict):
        self.coordinator = coordinator
        self._key = key
        self._config = config
        self._attr_unique_id = f"vmc_{key}"
        self._attr_name = config["name"]
        self._attr_icon = config["icon"]
        if config["device_class"]:
            self._attr_device_class = getattr(SensorDeviceClass, config["device_class"])
        if config["unit"]:
            self._attr_native_unit_of_measurement = config["unit"]
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        val = self.coordinator.data.get(self._key)
        if self._key == "modalita_gestione":
            return self.coordinator.data.get(self._key + "_text")
        return val

    async def async_update(self) -> None:
        await self.coordinator.async_refresh()
