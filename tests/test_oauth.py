"""Unit tests for the PKCE (RFC 7636) helpers in oauth.py."""

from __future__ import annotations

import base64
import hashlib
import re

from custom_components.ha_teams.oauth import (
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
    expected = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
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


def test_implementation_constructor_matches_ha_core_auth_implementation_signature() -> None:
    """Regression test for the ``AuthImplementation.__init__`` arity mismatch.

    Home Assistant core's ``AuthImplementation`` takes a single
    ``authorization_server`` object (not separate ``authorize_url``/
    ``token_url`` strings). Instantiating here with the real call shape
    catches a signature drift before it reaches production (see
    ``application_credentials.async_get_auth_implementation``).
    """
    from homeassistant.components.application_credentials import (
        AuthorizationServer,
        ClientCredential,
    )
    from homeassistant.core import HomeAssistant

    from custom_components.ha_teams.oauth import MicrosoftGraphPkceOAuth2Implementation

    server = AuthorizationServer(
        authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    )
    credential = ClientCredential(client_id="client-id", client_secret=None)

    impl = MicrosoftGraphPkceOAuth2Implementation(HomeAssistant(), "ha_teams", credential, server)

    assert impl.client_id == "client-id"
    assert impl.authorize_url == server.authorize_url
    assert impl.token_url == server.token_url
