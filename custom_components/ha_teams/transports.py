"""Transport-mode helpers for Microsoft Teams notifications."""

from __future__ import annotations

from .const import DEFAULT_TRANSPORT, TRANSPORT_GRAPH_DELEGATED, TRANSPORT_LABELS, TRANSPORT_TEAMS_BOT

SUPPORTED_TRANSPORTS = frozenset(TRANSPORT_LABELS)
KNOWN_TRANSPORTS = frozenset({TRANSPORT_GRAPH_DELEGATED, TRANSPORT_TEAMS_BOT})


def normalize_transport(value: str | None) -> str:
    """Return a supported transport, preserving backwards compatibility."""
    if value in SUPPORTED_TRANSPORTS:
        return value
    return DEFAULT_TRANSPORT


def transport_label(value: str | None) -> str:
    """Return a user-facing label for a transport."""
    return TRANSPORT_LABELS[normalize_transport(value)]
