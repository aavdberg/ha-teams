"""Unit tests for Teams transport-mode helpers."""

from __future__ import annotations

from custom_components.ha_teams.const import (
    DEFAULT_TRANSPORT,
    TRANSPORT_GRAPH_DELEGATED,
    TRANSPORT_TEAMS_BOT,
)
from custom_components.ha_teams.transports import (
    KNOWN_TRANSPORTS,
    SUPPORTED_TRANSPORTS,
    normalize_transport,
    transport_label,
)


def test_graph_delegated_is_the_default_and_supported_transport() -> None:
    assert DEFAULT_TRANSPORT == TRANSPORT_GRAPH_DELEGATED
    assert frozenset({TRANSPORT_GRAPH_DELEGATED}) == SUPPORTED_TRANSPORTS


def test_bot_transport_is_known_but_not_exposed_until_implemented() -> None:
    assert TRANSPORT_TEAMS_BOT in KNOWN_TRANSPORTS
    assert TRANSPORT_TEAMS_BOT not in SUPPORTED_TRANSPORTS


def test_normalize_transport_preserves_supported_values() -> None:
    assert normalize_transport(TRANSPORT_GRAPH_DELEGATED) == TRANSPORT_GRAPH_DELEGATED


def test_normalize_transport_defaults_missing_or_unknown_values_to_graph() -> None:
    assert normalize_transport(None) == TRANSPORT_GRAPH_DELEGATED
    assert normalize_transport("future_transport") == TRANSPORT_GRAPH_DELEGATED


def test_transport_label_uses_normalized_transport() -> None:
    assert transport_label(TRANSPORT_GRAPH_DELEGATED) == "Microsoft Graph (send as signed-in user)"
    assert transport_label(None) == "Microsoft Graph (send as signed-in user)"
    assert transport_label("future_transport") == "Microsoft Graph (send as signed-in user)"
