"""Thin Microsoft Graph API client used by the Teams integration."""

from __future__ import annotations

import asyncio
import json
import logging
import random
from typing import Any
from uuid import uuid4

from aiohttp import ClientSession
from homeassistant.helpers import config_entry_oauth2_flow

from .const import (
    ADAPTIVE_CARD_CONTENT_TYPE,
    DEFAULT_ADAPTIVE_CARD_VERSION,
    GRAPH_API_BASE,
    MAX_RETRY_ATTEMPTS,
    RETRY_BACKOFF_BASE_SECONDS,
    RETRY_BACKOFF_MAX_SECONDS,
)

_LOGGER = logging.getLogger(__name__)


class GraphApiError(Exception):
    """Raised when the Microsoft Graph API returns a (non-auth) error."""


class GraphAuthError(GraphApiError):
    """Raised on HTTP 401/403: token invalid, expired, or consent revoked.

    Callers (``__init__.py``, ``notify.py``) should translate this into a
    ``ConfigEntryAuthFailed`` so Home Assistant starts the reauth flow,
    instead of retrying indefinitely.
    """


def _should_retry(status: int) -> bool:
    """Return whether an HTTP status is worth retrying.

    Only transient failures (429 rate limiting, 5xx server errors) are
    retried. 4xx errors such as 400/401/403/404 indicate a permanent
    problem (bad request, auth failure, missing permission, deleted
    resource) and must not be retried blindly.
    """
    return status == 429 or 500 <= status < 600


def _backoff_delay(attempt: int) -> float:
    """Compute an exponential backoff delay (seconds) with jitter.

    ``attempt`` is 0-based (first retry = 0). Capped at
    ``RETRY_BACKOFF_MAX_SECONDS`` to avoid unbounded waits.
    """
    delay = min(RETRY_BACKOFF_BASE_SECONDS * (2**attempt), RETRY_BACKOFF_MAX_SECONDS)
    return delay + random.uniform(0, delay * 0.1)


def _build_adaptive_card_payload(card: dict[str, Any]) -> dict[str, Any]:
    """Build the Graph chatMessage payload for an Adaptive Card attachment.

    Graph expects the card JSON as a string inside ``attachments`` and an
    ``<attachment id="...">`` placeholder in the HTML body referencing it.
    """
    attachment_id = str(uuid4())
    return {
        "body": {
            "contentType": "html",
            "content": f'<attachment id="{attachment_id}"></attachment>',
        },
        "attachments": [
            {
                "id": attachment_id,
                "contentType": ADAPTIVE_CARD_CONTENT_TYPE,
                "content": json.dumps(card),
            }
        ],
    }


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
        """Perform a Graph API request with retry/backoff for transient errors.

        See "voorstel.md" section 12: retries HTTP 429 (respecting
        ``Retry-After``) and 5xx with exponential backoff + jitter, up to
        ``MAX_RETRY_ATTEMPTS``. HTTP 401/403 are raised immediately as
        ``GraphAuthError`` (no retry) so the caller can trigger reauth.
        """
        await self._oauth_session.async_ensure_token_valid()
        access_token = self._oauth_session.token["access_token"]
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = "Bearer " + access_token

        url = f"{GRAPH_API_BASE}{path}"

        for attempt in range(MAX_RETRY_ATTEMPTS):
            async with self._session.request(method, url, headers=headers, **kwargs) as resp:
                if resp.status == 204:
                    return None
                if resp.status in (401, 403):
                    body = await resp.text()
                    _LOGGER.debug("Graph API auth error %s for %s: %s", resp.status, url, body)
                    raise GraphAuthError(f"Graph API authentication/permission error ({resp.status}): {body}")
                if resp.status >= 400:
                    body = await resp.text()
                    if not _should_retry(resp.status) or attempt == MAX_RETRY_ATTEMPTS - 1:
                        _LOGGER.debug("Graph API error %s for %s: %s", resp.status, url, body)
                        raise GraphApiError(f"Graph API request failed ({resp.status}): {body}")
                    retry_after = resp.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else _backoff_delay(attempt)
                    _LOGGER.warning(
                        "Graph API request to %s failed with %s, retrying in %.1fs (attempt %d/%d)",
                        url,
                        resp.status,
                        delay,
                        attempt + 1,
                        MAX_RETRY_ATTEMPTS,
                    )
                    await asyncio.sleep(delay)
                    continue
                if resp.content_type == "application/json":
                    return await resp.json()
                return await resp.text()

        # Unreachable in practice: the loop above always returns or raises.
        raise GraphApiError(f"Graph API request to {url} failed after retries")

    async def async_list_joined_teams(self) -> list[dict[str, Any]]:
        """Return the teams the signed-in user is a member of."""
        result = await self._request("GET", "/me/joinedTeams")
        return result.get("value", []) if result else []

    async def async_list_channels(self, team_id: str) -> list[dict[str, Any]]:
        """Return the channels of a given team."""
        result = await self._request("GET", f"/teams/{team_id}/channels")
        return result.get("value", []) if result else []

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
        payload = _build_adaptive_card_payload(card)
        await self._request(
            "POST",
            f"/teams/{team_id}/channels/{channel_id}/messages",
            json=payload,
        )
