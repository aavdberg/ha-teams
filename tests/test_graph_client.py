"""Unit tests for the Graph HTTP transport's retry classification."""

from __future__ import annotations

import pytest

from custom_components.ha_teams.const import RETRY_BACKOFF_MAX_SECONDS
from custom_components.ha_teams.graph.client import _backoff_delay, _should_retry


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
