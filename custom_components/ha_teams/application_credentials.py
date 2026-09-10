"""Application credentials platform for Microsoft Teams (Graph API)."""

from __future__ import annotations

from homeassistant.components.application_credentials import (
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant

from .const import OAUTH2_AUTHORIZE_TEMPLATE, OAUTH2_TOKEN_TEMPLATE
from .oauth import MicrosoftGraphPkceOAuth2Implementation
from .tenant_store import async_get_tenant


async def _async_get_authorization_server(hass: HomeAssistant, auth_domain: str) -> AuthorizationServer:
    """Return the authorization server for the credential's Microsoft Entra tenant.

    Defaults to the multi-tenant "common" endpoint, but single-tenant app
    registrations ("Accounts in this organizational directory only") must
    authenticate against their own tenant-specific endpoint -- the config
    flow asks for this (see ``tenant_store.py``) before starting login.
    """
    tenant = await async_get_tenant(hass, auth_domain)
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE_TEMPLATE.format(tenant=tenant),
        token_url=OAUTH2_TOKEN_TEMPLATE.format(tenant=tenant),
    )


async def async_get_authorization_server(hass: HomeAssistant) -> AuthorizationServer:
    """Return the default authorization server for Application Credentials UI text."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE_TEMPLATE.format(tenant="common"),
        token_url=OAUTH2_TOKEN_TEMPLATE.format(tenant="common"),
    )


async def async_get_auth_implementation(hass: HomeAssistant, auth_domain: str, credential: ClientCredential):
    """Return a PKCE-enabled OAuth2 implementation for this integration."""
    server = await _async_get_authorization_server(hass, auth_domain)
    return MicrosoftGraphPkceOAuth2Implementation(
        hass,
        auth_domain,
        credential,
        server,
    )


async def async_get_description_placeholders(hass: HomeAssistant) -> dict[str, str]:
    """Return placeholders used in the application credentials UI text."""
    return {
        "authorize_url": OAUTH2_AUTHORIZE_TEMPLATE.format(tenant="common"),
        "token_url": OAUTH2_TOKEN_TEMPLATE.format(tenant="common"),
        "more_info_url": "https://github.com/aavdberg/ha-teams#setup",
        "redirect_url": "https://my.home-assistant.io/redirect/oauth",
    }
