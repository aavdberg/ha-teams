"""The Microsoft Teams integration."""
from __future__ import annotations

import logging
from dataclasses import dataclass

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import ConfigEntryAuthFailed, ServiceValidationError
from homeassistant.helpers import aiohttp_client, config_entry_oauth2_flow

from .api import GraphAuthError, TeamsGraphApiClient
from .const import ATTR_CARD, ATTR_CONFIG_ENTRY_ID, CONF_CHANNEL_ID, CONF_TEAM_ID, DOMAIN, SERVICE_SEND_CARD

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.NOTIFY]

SERVICE_SEND_CARD_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_CONFIG_ENTRY_ID): str,
        vol.Required(ATTR_CARD): dict,
    }
)


@dataclass
class TeamsRuntimeData:
    """Runtime data stored on the config entry."""

    client: TeamsGraphApiClient
    team_id: str
    channel_id: str


type TeamsConfigEntry = ConfigEntry[TeamsRuntimeData]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register integration-wide services (once, not per config entry)."""

    async def _async_handle_send_card(call: ServiceCall) -> None:
        """Handle the ``ha_teams.send_card`` service call.

        See "voorstel.md" section 9.3: allows sending a full Adaptive Card
        (not just plain text) to the channel configured on a given entry.
        """
        entry_id = call.data[ATTR_CONFIG_ENTRY_ID]
        entry = hass.config_entries.async_get_entry(entry_id)
        if entry is None or entry.domain != DOMAIN:
            raise ServiceValidationError(f"Unknown ha_teams config entry: {entry_id}")

        runtime: TeamsRuntimeData = entry.runtime_data
        try:
            await runtime.client.async_send_adaptive_card(
                runtime.team_id, runtime.channel_id, call.data[ATTR_CARD]
            )
        except GraphAuthError as err:
            raise ConfigEntryAuthFailed("Microsoft Teams authentication failed") from err

    hass.services.async_register(
        DOMAIN, SERVICE_SEND_CARD, _async_handle_send_card, schema=SERVICE_SEND_CARD_SCHEMA
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: TeamsConfigEntry) -> bool:
    """Set up Microsoft Teams from a config entry."""
    implementation = await config_entry_oauth2_flow.async_get_config_entry_implementation(
        hass, entry
    )
    oauth_session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
    try:
        # Ensures the access token is valid (refreshing via the token
        # endpoint, no user interaction) before the first API call is made.
        await oauth_session.async_ensure_token_valid()
    except Exception as err:  # noqa: BLE001
        # Token refresh failed (e.g. the user revoked consent in Entra ID,
        # or the refresh token expired). Ask Home Assistant to start the
        # reauth flow rather than leaving the entry in a broken state.
        raise ConfigEntryAuthFailed("Failed to refresh Microsoft Teams token") from err

    session = aiohttp_client.async_get_clientsession(hass)
    client = TeamsGraphApiClient(session, oauth_session)

    team_id = entry.options.get(CONF_TEAM_ID) or entry.data.get(CONF_TEAM_ID)
    channel_id = entry.options.get(CONF_CHANNEL_ID) or entry.data.get(CONF_CHANNEL_ID)

    entry.runtime_data = TeamsRuntimeData(client=client, team_id=team_id, channel_id=channel_id)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def _async_update_listener(hass: HomeAssistant, entry: TeamsConfigEntry) -> None:
    """Reload the entry when its options (e.g. selected channel) change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: TeamsConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
