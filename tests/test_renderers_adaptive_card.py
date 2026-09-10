"""Unit tests for the Adaptive Card payload renderer."""

from __future__ import annotations

import json

from custom_components.ha_teams.const import ADAPTIVE_CARD_CONTENT_TYPE
from custom_components.ha_teams.renderers.adaptive_card import build_adaptive_card_payload


def test_adaptive_card_payload_references_attachment_by_id() -> None:
    card = {"type": "AdaptiveCard", "body": [{"type": "TextBlock", "text": "hi"}]}
    payload = build_adaptive_card_payload(card)

    assert payload["body"]["contentType"] == "html"
    attachment = payload["attachments"][0]
    assert attachment["contentType"] == ADAPTIVE_CARD_CONTENT_TYPE
    assert attachment["id"] in payload["body"]["content"]
    assert json.loads(attachment["content"]) == card


def test_adaptive_card_payload_has_unique_attachment_ids() -> None:
    card = {"type": "AdaptiveCard", "body": []}
    payload_1 = build_adaptive_card_payload(card)
    payload_2 = build_adaptive_card_payload(card)
    assert payload_1["attachments"][0]["id"] != payload_2["attachments"][0]["id"]
