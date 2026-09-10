"""Unit tests for Teams destination validation."""

from __future__ import annotations

import pytest
from homeassistant.exceptions import ServiceValidationError

from custom_components.ha_teams.destination import has_configured_destination, require_configured_destination


def test_require_configured_destination_returns_team_and_channel() -> None:
    assert require_configured_destination("team-id", "channel-id") == ("team-id", "channel-id")


def test_require_configured_destination_strips_whitespace() -> None:
    assert require_configured_destination(" team-id ", "\tchannel-id\n") == ("team-id", "channel-id")


def test_has_configured_destination_matches_validation() -> None:
    assert has_configured_destination("team-id", "channel-id") is True
    assert has_configured_destination(" team-id ", " channel-id ") is True
    assert has_configured_destination(" ", "channel-id") is False
    assert has_configured_destination("team-id", " ") is False


@pytest.mark.parametrize(
    ("team_id", "channel_id", "missing"),
    [
        (None, "channel-id", "select a Team"),
        ("team-id", None, "select a Channel"),
        (None, None, "select a Team and a Channel"),
        ("", "channel-id", "select a Team"),
        ("team-id", "", "select a Channel"),
        (" ", "channel-id", "select a Team"),
        ("team-id", " ", "select a Channel"),
        (" ", " ", "select a Team and a Channel"),
    ],
)
def test_require_configured_destination_raises_actionable_error(
    team_id: str | None, channel_id: str | None, missing: str
) -> None:
    with pytest.raises(ServiceValidationError, match="destination is not configured") as exc_info:
        require_configured_destination(team_id, channel_id)

    message = str(exc_info.value)
    assert missing in message
    assert "Settings > Devices & services > Microsoft Teams > Configure" in message
