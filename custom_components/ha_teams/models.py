"""Data models shared across the integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry

from .graph import TeamsGraphApiClient


@dataclass
class TeamsRuntimeData:
    """Runtime data stored on the config entry."""

    client: TeamsGraphApiClient
    team_id: str
    channel_id: str


type TeamsConfigEntry = ConfigEntry[TeamsRuntimeData]
