"""Diagnostics support for Microsoft Teams.

Redacts anything sensitive (tokens, IDs) so users can safely attach
diagnostics to bug reports.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_CHANNEL_ID, CONF_TEAM_ID

TO_REDACT = {
    "access_token",
    "refresh_token",
    "id_token",
    "auth_implementation",
    CONF_TEAM_ID,
    CONF_CHANNEL_ID,
}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """Return diagnostics for a config entry, with secrets/IDs redacted."""
    return {
        "entry_data": async_redact_data(dict(entry.data), TO_REDACT),
        "entry_options": async_redact_data(dict(entry.options), TO_REDACT),
    }
