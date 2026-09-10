"""Destination validation helpers for Microsoft Teams messages."""

from __future__ import annotations

from homeassistant.exceptions import ServiceValidationError


def normalize_destination_id(value: str | None) -> str | None:
    """Normalize a stored Team or Channel ID."""
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def has_configured_destination(team_id: str | None, channel_id: str | None) -> bool:
    """Return whether both Teams destination IDs are configured."""
    return normalize_destination_id(team_id) is not None and normalize_destination_id(channel_id) is not None


def require_configured_destination(team_id: str | None, channel_id: str | None) -> tuple[str, str]:
    """Return the configured Teams destination or raise a user-facing error."""
    normalized_team_id = normalize_destination_id(team_id)
    normalized_channel_id = normalize_destination_id(channel_id)
    if normalized_team_id and normalized_channel_id:
        return normalized_team_id, normalized_channel_id

    if not normalized_team_id and not normalized_channel_id:
        missing_text = "a Team and a Channel"
    elif not normalized_team_id:
        missing_text = "a Team"
    else:
        missing_text = "a Channel"
    raise ServiceValidationError(
        f"Microsoft Teams destination is not configured. Open Settings > Devices & services > "
        f"Microsoft Teams > Configure and select {missing_text} before sending notifications."
    )
