"""Unit tests for Graph API retry classification and Adaptive Card payloads."""
from __future__ import annotations

import json

import pytest

from custom_components.ha_teams.api import (
    _backoff_delay,
    _build_adaptive_card_payload,
    _should_retry,
)
from custom_components.ha_teams.const import (
    ADAPTIVE_CARD_CONTENT_TYPE,
    RETRY_BACKOFF_MAX_SECONDS,
)


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504, 599])
def test_transient_statuses_are_retried(status: int) -> None:
    assert _should_retry(status) is True


@pytest.mark.parametrize("status", [200, 400, 401, 403, 404, 409, 422])
def test_permanent_statuses_are_not_retried(status: int) -> None:
    assert _should_retry(status) is False


def test_backoff_delay_grows_exponentially_and_is_capped() -> None:
    delay_0 = _backoff_delay(0)
    delay_1 = _backoff_delay(1)
    delay_2 = _backoff_delay(2)
    # Jitter adds up to 10%, so compare using the base (unjittered) trend.
    assert delay_0 < delay_1 < delay_2
    # Even for a very high attempt count, delay must never exceed the cap
    # by more than the jitter margin.
    huge_delay = _backoff_delay(20)
    assert huge_delay <= RETRY_BACKOFF_MAX_SECONDS * 1.1


def test_adaptive_card_payload_references_attachment_by_id() -> None:
    card = {"type": "AdaptiveCard", "body": [{"type": "TextBlock", "text": "hi"}]}
    payload = _build_adaptive_card_payload(card)

    assert payload["body"]["contentType"] == "html"
    attachment = payload["attachments"][0]
    assert attachment["contentType"] == ADAPTIVE_CARD_CONTENT_TYPE
    assert attachment["id"] in payload["body"]["content"]
    assert json.loads(attachment["content"]) == card


def test_adaptive_card_payload_has_unique_attachment_ids() -> None:
    card = {"type": "AdaptiveCard", "body": []}
    payload_1 = _build_adaptive_card_payload(card)
    payload_2 = _build_adaptive_card_payload(card)
    assert payload_1["attachments"][0]["id"] != payload_2["attachments"][0]["id"]
