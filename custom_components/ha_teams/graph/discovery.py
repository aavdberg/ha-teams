"""Team and channel discovery endpoints of the Microsoft Graph API."""

from __future__ import annotations

from typing import Any


class GraphDiscoveryMixin:
    """Endpoints for listing the Teams/Channels the user can post to.

    Mixed into :class:`~custom_components.ha_teams.graph.TeamsGraphApiClient`,
    which also provides ``_request`` via ``GraphHttpClient``.
    """

    async def async_list_joined_teams(self) -> list[dict[str, Any]]:
        """Return the teams the signed-in user is a member of."""
        result = await self._request("GET", "/me/joinedTeams")
        return result.get("value", []) if result else []

    async def async_list_channels(self, team_id: str) -> list[dict[str, Any]]:
        """Return the channels of a given team."""
        result = await self._request("GET", f"/teams/{team_id}/channels")
        return result.get("value", []) if result else []
