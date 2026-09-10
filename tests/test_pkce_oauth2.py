"""Unit tests for the PKCE (RFC 7636) helpers in pkce_oauth2.py."""
from __future__ import annotations

import base64
import hashlib
import re

from custom_components.ha_teams.pkce_oauth2 import (
    _CODE_VERIFIER_LENGTH,
    _code_challenge,
    _generate_code_verifier,
)

# RFC 7636 requires the code_verifier to use only unreserved URL characters.
_ALLOWED_VERIFIER_CHARS = re.compile(r"^[A-Za-z0-9\-._~]+$")


def test_code_verifier_is_url_safe_and_sufficiently_long() -> None:
    verifier = _generate_code_verifier()
    assert _ALLOWED_VERIFIER_CHARS.match(verifier)
    # RFC 7636 mandates 43-128 chars; token_urlsafe(64) comfortably exceeds 43.
    assert 43 <= len(verifier) <= 128


def test_code_verifier_is_random_each_time() -> None:
    verifiers = {_generate_code_verifier() for _ in range(20)}
    assert len(verifiers) == 20


def test_code_challenge_matches_manual_s256_computation() -> None:
    verifier = "a" * _CODE_VERIFIER_LENGTH
    expected = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest())
        .rstrip(b"=")
        .decode("ascii")
    )
    assert _code_challenge(verifier) == expected


def test_code_challenge_has_no_padding_and_is_deterministic() -> None:
    verifier = _generate_code_verifier()
    challenge_1 = _code_challenge(verifier)
    challenge_2 = _code_challenge(verifier)
    assert challenge_1 == challenge_2
    assert "=" not in challenge_1
    assert _ALLOWED_VERIFIER_CHARS.match(challenge_1)


def test_different_verifiers_produce_different_challenges() -> None:
    assert _code_challenge("a" * 43) != _code_challenge("b" * 43)
