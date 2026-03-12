import logging
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_SLAVE_ID

_LOGGER = logging.getLogger(__name__)


class VMCConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow VMC."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Step iniziale."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            slave = user_input[CONF_SLAVE_ID]

            _LOGGER.info("VMC config: %s:%s slave %s", host, port, slave)

            await self.async_set_unique_id(f"vmc_{host}_{port}_{slave}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"VMC {host}:{port}",
                data={
                    CONF_HOST: host,
                    CONF_PORT: port,
                    CONF_SLAVE_ID: slave,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default="192.168.1.200"): str,
                vol.Required(CONF_PORT, default=502): int,
                vol.Required(CONF_SLAVE_ID, default=1): int,
            }),
            errors=errors,
        )
