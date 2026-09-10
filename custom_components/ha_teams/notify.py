"""Notify platform for Microsoft Teams."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.notify import NotifyEntity, NotifyEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import GraphApiError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Teams notify entity from a config entry."""
    runtime = entry.runtime_data
    async_add_entities([TeamsNotifyEntity(entry, runtime)])


class TeamsNotifyEntity(NotifyEntity):
    """Notify entity that posts messages to a Microsoft Teams channel."""

    _attr_has_entity_name = True
    entity_description = NotifyEntityDescription(key="channel_message", name=None)

    def __init__(self, entry: ConfigEntry, runtime) -> None:
        """Initialize the notify entity."""
        self._runtime = runtime
        self._attr_unique_id = f"{entry.entry_id}_notify"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "Microsoft",
            "model": "Teams channel",
        }

    async def async_send_message(self, message: str, title: str | None = None) -> None:
        """Send a message to the configured Teams channel."""
        text = f"**{title}**\n\n{message}" if title else message
        try:
            await self._runtime.client.async_send_channel_message(
                self._runtime.team_id, self._runtime.channel_id, text
            )
        except GraphApiError as err:
            _LOGGER.error("Failed to send Teams message: %s", err)
            raise
