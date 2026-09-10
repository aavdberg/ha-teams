"""Unit tests for the plain-text message renderer."""

from __future__ import annotations

from custom_components.ha_teams.renderers.text import build_text_message


def test_build_text_message_without_title_returns_message_unchanged() -> None:
    assert build_text_message("hello world") == "hello world"


def test_build_text_message_with_title_prefixes_bold_markdown() -> None:
    result = build_text_message("hello world", title="Front door")
    assert result == "**Front door**\n\nhello world"
