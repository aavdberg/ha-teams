"""The Microsoft Teams integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client, config_entry_oauth2_flow

from .api import TeamsGraphApiClient
from .const import CONF_CHANNEL_ID, CONF_TEAM_ID, DOMAIN

PLATFORMS: list[Platform] = [Platform.NOTIFY]


@dataclass
class TeamsRuntimeData:
    """Runtime data stored on the config entry."""

    client: TeamsGraphApiClient
    team_id: str
    channel_id: str


type TeamsConfigEntry = ConfigEntry[TeamsRuntimeData]


async def async_setup_entry(hass: HomeAssistant, entry: TeamsConfigEntry) -> bool:
    """Set up Microsoft Teams from a config entry."""
    implementation = await config_entry_oauth2_flow.async_get_config_entry_implementation(
        hass, entry
    )
    oauth_session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
    # Ensures the access token is valid (refreshing via the token endpoint,
    # no user interaction) before the first API call is made.
    await oauth_session.async_ensure_token_valid()

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
