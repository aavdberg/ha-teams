"""Thin Microsoft Graph API client used by the Teams integration."""
from __future__ import annotations

import logging
from typing import Any

from aiohttp import ClientResponseError, ClientSession

from homeassistant.helpers import config_entry_oauth2_flow

from .const import GRAPH_API_BASE

_LOGGER = logging.getLogger(__name__)


class GraphApiError(Exception):
    """Raised when the Microsoft Graph API returns an error."""


class TeamsGraphApiClient:
    """Small wrapper around the Graph API endpoints this integration needs."""

    def __init__(
        self,
        session: ClientSession,
        oauth_session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize the API client.

        ``oauth_session`` transparently refreshes the access token before it
        expires, so callers never need to think about token lifetime.
        """
        self._session = session
        self._oauth_session = oauth_session

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        await self._oauth_session.async_ensure_token_valid()
        access_token = self._oauth_session.token["access_token"]
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {access_token}"

        url = f"{GRAPH_API_BASE}{path}"
        async with self._session.request(method, url, headers=headers, **kwargs) as resp:
            if resp.status == 204:
                return None
            try:
                resp.raise_for_status()
            except ClientResponseError as err:
                body = await resp.text()
                _LOGGER.debug("Graph API error %s for %s: %s", err.status, url, body)
                raise GraphApiError(f"Graph API request failed ({err.status}): {body}") from err
            if resp.content_type == "application/json":
                return await resp.json()
            return await resp.text()

    async def async_list_joined_teams(self) -> list[dict[str, Any]]:
        """Return the teams the signed-in user is a member of."""
        result = await self._request("GET", "/me/joinedTeams")
        return result.get("value", []) if result else []

    async def async_list_channels(self, team_id: str) -> list[dict[str, Any]]:
        """Return the channels of a given team."""
        result = await self._request("GET", f"/teams/{team_id}/channels")
        return result.get("value", []) if result else []

    async def async_send_channel_message(
        self, team_id: str, channel_id: str, message: str
    ) -> None:
        """Post a plain-text message to a Teams channel."""
        payload = {"body": {"contentType": "text", "content": message}}
        await self._request(
            "POST",
            f"/teams/{team_id}/channels/{channel_id}/messages",
            json=payload,
        )
