"""Destination validation helpers for Microsoft Teams messages."""

from __future__ import annotations

from homeassistant.exceptions import ServiceValidationError


def require_configured_destination(team_id: str | None, channel_id: str | None) -> tuple[str, str]:
    """Return the configured Teams destination or raise a user-facing error."""
    if team_id and channel_id:
        return team_id, channel_id

    missing = []
    if not team_id:
        missing.append("Team")
    if not channel_id:
        missing.append("Channel")
    missing_text = " and ".join(missing)
    raise ServiceValidationError(
        f"Microsoft Teams destination is not configured. Open Settings > Devices & services > "
        f"Microsoft Teams > Configure and select a {missing_text} before sending notifications."
    )
