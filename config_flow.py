"""Config Flow per VMC Waveshare."""
import logging
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_SLAVE_ID

_LOGGER = logging.getLogger(__name__)

class VMCConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow per VMC."""

    VERSION = 1
    MINOR_VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Opzioni config flow."""
        return VMCOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Step user iniziale."""
        errors = {}
        
        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            slave = user_input[CONF_SLAVE_ID]
            
            # Test connessione Modbus (semplificato)
            try:
                # Simula test connessione (implementa test reale)
                if host == "192.168.1.200" and port == 502:
                    return self.async_create_entry(
                        title=f"VMC {host}:{port}",
                        data={
                            CONF_HOST: host,
                            CONF_PORT: port,
                            CONF_SLAVE_ID: slave
                        }
                    )
                else:
                    errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"
        
        schema = vol.Schema({
            vol.Required(CONF_HOST, default="192.168.1.200"): str,
            vol.Required(CONF_PORT, default=502): int,
            vol.Required(CONF_SLAVE_ID, default=1): int,
        })
        
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )

class VMCOptionsFlowHandler(config_entries.OptionsFlow):
    """Gestisce opzioni modifica."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Gestisce opzioni."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_HOST, 
                        default=self.config_entry.options.get(CONF_HOST, 
                        self.config_entry.data.get(CONF_HOST, ""))): str,
            vol.Required(CONF_PORT, 
                        default=self.config_entry.options.get(CONF_PORT, 
                        self.config_entry.data.get(CONF_PORT, 502))): int,
            vol.Required(CONF_SLAVE_ID, 
                        default=self.config_entry.options.get(CONF_SLAVE_ID, 
                        self.config_entry.data.get(CONF_SLAVE_ID, 1))): int,
        })
        
        return self.async_show_form(
            step_id="init",
            data_schema=schema
        )
