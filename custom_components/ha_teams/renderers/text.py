"""Plain-text message rendering for the notify platform."""

from __future__ import annotations


def build_text_message(message: str, title: str | None = None) -> str:
    """Render a Home Assistant notification as Markdown text.

    Teams channel messages support a small Markdown subset; a bold title
    line followed by the message body is the simplest readable format.
    """
    return f"**{title}**\n\n{message}" if title else message
