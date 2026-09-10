"""Data models shared across the integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry

from .graph import TeamsGraphApiClient


@dataclass
class TeamsRuntimeData:
    """Runtime data stored on the config entry."""

    client: TeamsGraphApiClient
    transport: str
    team_id: str | None
    channel_id: str | None


type TeamsConfigEntry = ConfigEntry[TeamsRuntimeData]
