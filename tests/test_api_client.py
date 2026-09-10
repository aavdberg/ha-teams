"""Unit test for the adaptive card version default in the Graph client."""
from __future__ import annotations

import asyncio
import json

from custom_components.ha_teams.api import TeamsGraphApiClient
from custom_components.ha_teams.const import DEFAULT_ADAPTIVE_CARD_VERSION


class _FakeOAuthSession:
    def __init__(self) -> None:
        self.token = {"access_token": "fake-token"}
        self.ensure_calls = 0

    async def async_ensure_token_valid(self) -> None:
        self.ensure_calls += 1


class _FakeResponse:
    def __init__(self, status: int, json_body: dict | None = None) -> None:
        self.status = status
        self.headers: dict[str, str] = {}
        self.content_type = "application/json"
        self._json_body = json_body or {}

    async def __aenter__(self) -> "_FakeResponse":
        return self

    async def __aexit__(self, *exc_info) -> None:
        return None

    async def json(self) -> dict:
        return self._json_body

    async def text(self) -> str:
        return json.dumps(self._json_body)


class _FakeSession:
    """Captures the last request made, always returning HTTP 201."""

    def __init__(self) -> None:
        self.last_request: dict | None = None

    def request(self, method: str, url: str, **kwargs):
        self.last_request = {"method": method, "url": url, **kwargs}
        return _FakeResponse(status=201, json_body={"id": "message-1"})


def test_send_adaptive_card_defaults_version_when_missing() -> None:
    session = _FakeSession()
    oauth_session = _FakeOAuthSession()
    client = TeamsGraphApiClient(session, oauth_session)

    asyncio.run(
        client.async_send_adaptive_card(
            "team-1", "channel-1", {"type": "AdaptiveCard", "body": []}
        )
    )

    sent_payload = session.last_request["json"]
    card_sent = json.loads(sent_payload["attachments"][0]["content"])
    assert card_sent["version"] == DEFAULT_ADAPTIVE_CARD_VERSION


def test_send_adaptive_card_keeps_explicit_version() -> None:
    session = _FakeSession()
    oauth_session = _FakeOAuthSession()
    client = TeamsGraphApiClient(session, oauth_session)

    asyncio.run(
        client.async_send_adaptive_card(
            "team-1", "channel-1", {"type": "AdaptiveCard", "version": "1.4", "body": []}
        )
    )

    sent_payload = session.last_request["json"]
    card_sent = json.loads(sent_payload["attachments"][0]["content"])
    assert card_sent["version"] == "1.4"
