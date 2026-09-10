"""Placeholder: inbound webhook handler for Adaptive Card action callbacks.

Not implemented yet. Would register an HA webhook (or aiohttp view) that
Microsoft Teams calls when a user taps a card action (e.g. "Acknowledge"),
translate the payload into an HA event/service call, and return the
required ``CardAction`` response so Teams updates the card in place.

Must validate the request first — see ``validation.py`` — before acting on
any callback payload.
"""

from __future__ import annotations
