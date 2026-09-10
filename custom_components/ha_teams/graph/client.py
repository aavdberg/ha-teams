"""Low-level Microsoft Graph HTTP transport: retry/backoff and auth errors.

This module only knows how to make an authenticated, retried HTTP request
against the Graph API. Endpoint-specific behaviour (discovery, messaging,
...) lives in sibling modules that mix into :class:`GraphHttpClient`.
"""

from __future__ import annotations

import asyncio
import logging
import random
from typing import Any

from aiohttp import ClientSession
from homeassistant.helpers import config_entry_oauth2_flow

from ..const import GRAPH_API_BASE, MAX_RETRY_ATTEMPTS, RETRY_BACKOFF_BASE_SECONDS, RETRY_BACKOFF_MAX_SECONDS

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


class GraphHttpClient:
    """Authenticated, retrying HTTP transport for the Microsoft Graph API."""

    def __init__(
        self,
        session: ClientSession,
        oauth_session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize the transport.

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
