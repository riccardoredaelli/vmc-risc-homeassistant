"""Integrazione VMC Waveshare RS485."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from .coordinator import VMCDataUpdateCoordinator
from .const import DOMAIN

PLATFORMS = [Platform.SENSOR, Platform.FAN, Platform.CLIMATE]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup entry."""
    coordinator = VMCDataUpdateCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

class VMCConfigFlow:
    # Config flow per UI setup (aggiungi config_flow.py completo se vuoi)
    pass
