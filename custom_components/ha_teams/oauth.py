"""OAuth2 implementation that adds PKCE (RFC 7636) support.

Home Assistant's built-in ``config_entry_oauth2_flow.LocalOAuth2Implementation``
does not add a PKCE code_verifier/code_challenge pair to the authorization
request. Microsoft Entra ID (Azure AD) app registrations configured as a
"public client" (mobile/desktop, no client secret) require PKCE, and using it
even for confidential clients is best practice. This module layers PKCE on
top of the standard implementation without needing a client secret.
"""

from __future__ import annotations

import base64
import hashlib
import secrets
from typing import Any

from homeassistant.components.application_credentials import (
    AuthImplementation,
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant

_CODE_VERIFIER_LENGTH = 64


def _generate_code_verifier() -> str:
    """Generate a high-entropy PKCE code verifier."""
    return secrets.token_urlsafe(_CODE_VERIFIER_LENGTH)


def _code_challenge(verifier: str) -> str:
    """Derive the S256 PKCE code challenge from a verifier."""
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


class MicrosoftGraphPkceOAuth2Implementation(AuthImplementation):
    """Local OAuth2 implementation using Authorization Code + PKCE.

    A ``code_verifier`` is generated per authorization attempt and stored on
    the instance so it can be attached to the subsequent token exchange. This
    mirrors the recommended flow for public clients registered in Microsoft
    Entra ID, removing the need to store/rotate a client secret.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        auth_domain: str,
        credential: ClientCredential,
        authorization_server: AuthorizationServer,
    ) -> None:
        """Initialize the PKCE OAuth2 implementation."""
        super().__init__(hass, auth_domain, credential, authorization_server)
        self._code_verifier: str | None = None

    @property
    def extra_authorize_data(self) -> dict[str, Any]:
        """Extra data to append to the authorize url, including PKCE + scopes."""
        self._code_verifier = _generate_code_verifier()
        return {
            "scope": " ".join(self._scopes()),
            "code_challenge": _code_challenge(self._code_verifier),
            "code_challenge_method": "S256",
            # Forces the account picker; helps users pick the right tenant.
            "prompt": "select_account",
        }

    def _scopes(self) -> list[str]:
        from .const import OAUTH2_SCOPES

        return OAUTH2_SCOPES

    async def async_resolve_external_data(self, external_data: Any) -> dict:
        """Resolve the authorization code, attaching the PKCE code_verifier."""
        data = {
            "grant_type": "authorization_code",
            "code": external_data["code"],
            "redirect_uri": external_data["state"]["redirect_uri"],
            "code_verifier": self._code_verifier,
        }
        return await self._token_request(data)

    async def _async_refresh_token(self, token: dict) -> dict:
        """Refresh an existing token.

        No code_verifier is required for refresh_token grants, so the
        default behaviour from AuthImplementation is sufficient; this is
        kept explicit for clarity/documentation purposes.
        """
        return await super()._async_refresh_token(token)
