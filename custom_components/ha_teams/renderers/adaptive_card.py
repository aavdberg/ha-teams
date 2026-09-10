"""Adaptive Card payload rendering for Microsoft Graph chat messages."""

from __future__ import annotations

import json
from typing import Any
from uuid import uuid4

from ..const import ADAPTIVE_CARD_CONTENT_TYPE


def build_adaptive_card_payload(card: dict[str, Any]) -> dict[str, Any]:
    """Build the Graph chatMessage payload for an Adaptive Card attachment.

    Graph expects the card JSON as a string inside ``attachments`` and an
    ``<attachment id="...">`` placeholder in the HTML body referencing it.
    """
    attachment_id = str(uuid4())
    return {
        "body": {
            "contentType": "html",
            "content": f'<attachment id="{attachment_id}"></attachment>',
        },
        "attachments": [
            {
                "id": attachment_id,
                "contentType": ADAPTIVE_CARD_CONTENT_TYPE,
                "content": json.dumps(card),
            }
        ],
    }
