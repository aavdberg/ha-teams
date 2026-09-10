"""Unit tests for Teams destination validation."""

from __future__ import annotations

import pytest
from homeassistant.exceptions import ServiceValidationError

from custom_components.ha_teams.destination import require_configured_destination


def test_require_configured_destination_returns_team_and_channel() -> None:
    assert require_configured_destination("team-id", "channel-id") == ("team-id", "channel-id")


@pytest.mark.parametrize(
    ("team_id", "channel_id", "missing"),
    [
        (None, "channel-id", "Team"),
        ("team-id", None, "Channel"),
        (None, None, "Team and Channel"),
        ("", "channel-id", "Team"),
        ("team-id", "", "Channel"),
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
