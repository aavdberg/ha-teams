"""Sending plain-text and Adaptive Card messages via the Microsoft Graph API."""

from __future__ import annotations

from typing import Any

from ..const import DEFAULT_ADAPTIVE_CARD_VERSION
from ..renderers.adaptive_card import build_adaptive_card_payload


class GraphMessagesMixin:
    """Endpoints for posting channel messages.

    Mixed into :class:`~custom_components.ha_teams.graph.TeamsGraphApiClient`,
    which also provides ``_request`` via ``GraphHttpClient``.
    """

    async def async_send_channel_message(self, team_id: str, channel_id: str, message: str) -> None:
        """Post a plain-text message to a Teams channel."""
        payload = {"body": {"contentType": "text", "content": message}}
        await self._request(
            "POST",
            f"/teams/{team_id}/channels/{channel_id}/messages",
            json=payload,
        )

    async def async_send_adaptive_card(
        self,
        team_id: str,
        channel_id: str,
        card: dict[str, Any],
        card_version: str = DEFAULT_ADAPTIVE_CARD_VERSION,
    ) -> None:
        """Post a full Adaptive Card to a Teams channel.

        ``card`` is the raw Adaptive Card JSON (schema/body/actions); if it
        has no ``version`` key, ``card_version`` is used as a default.
        """
        if "version" not in card:
            card = {**card, "version": card_version}
        payload = build_adaptive_card_payload(card)
        await self._request(
            "POST",
            f"/teams/{team_id}/channels/{channel_id}/messages",
            json=payload,
        )
