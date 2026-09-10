"""Application credentials platform for Microsoft Teams (Graph API)."""

from __future__ import annotations

from homeassistant.components.application_credentials import (
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant

from .const import DEFAULT_TENANT, OAUTH2_AUTHORIZE_TEMPLATE, OAUTH2_TOKEN_TEMPLATE
from .pkce_oauth2 import MicrosoftGraphPkceOAuth2Implementation


async def async_get_authorization_server(hass: HomeAssistant) -> AuthorizationServer:
    """Return the default (multi-tenant "common") authorization server.

    Users who register a single-tenant Azure AD app can still authenticate;
    Microsoft will redirect/validate the tenant during login. Advanced users
    who need a specific tenant endpoint can fork this or open an issue to
    make it configurable per credential.
    """
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE_TEMPLATE.format(tenant=DEFAULT_TENANT),
        token_url=OAUTH2_TOKEN_TEMPLATE.format(tenant=DEFAULT_TENANT),
    )


async def async_get_auth_implementation(hass: HomeAssistant, auth_domain: str, credential: ClientCredential):
    """Return a PKCE-enabled OAuth2 implementation for this integration."""
    server = await async_get_authorization_server(hass)
    return MicrosoftGraphPkceOAuth2Implementation(
        hass,
        auth_domain,
        credential,
        server.authorize_url,
        server.token_url,
    )


async def async_get_description_placeholders(hass: HomeAssistant) -> dict[str, str]:
    """Return placeholders used in the application credentials UI text."""
    return {
        "authorize_url": OAUTH2_AUTHORIZE_TEMPLATE.format(tenant=DEFAULT_TENANT),
        "token_url": OAUTH2_TOKEN_TEMPLATE.format(tenant=DEFAULT_TENANT),
        "more_info_url": "https://github.com/aavdberg/ha-teams#setup",
        "redirect_url": "https://my.home-assistant.io/redirect/oauth",
    }
