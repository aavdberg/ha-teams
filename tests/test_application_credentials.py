"""Unit tests for application_credentials.py's tenant-aware authorization server.

Regression coverage for ``AADSTS50194`` ("Application ... is not
configured as a multi-tenant application. Usage of the /common endpoint is
not supported for such applications"), reported when a user's single-tenant
Microsoft Entra app registration hit the previously hardcoded ``/common``
endpoint.
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from custom_components.ha_teams.application_credentials import _async_get_authorization_server
from custom_components.ha_teams.tenant_store import async_set_tenant


async def test_authorization_server_uses_common_tenant_by_default() -> None:
    server = await _async_get_authorization_server(HomeAssistant(), "ha_teams.client-a")

    assert server.authorize_url == "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    assert server.token_url == "https://login.microsoftonline.com/common/oauth2/v2.0/token"


async def test_authorization_server_uses_persisted_single_tenant_id() -> None:
    hass = HomeAssistant()
    await async_set_tenant(hass, "ha_teams.client-a", "contoso.onmicrosoft.com")

    server = await _async_get_authorization_server(hass, "ha_teams.client-a")

    assert server.authorize_url == "https://login.microsoftonline.com/contoso.onmicrosoft.com/oauth2/v2.0/authorize"
    assert server.token_url == "https://login.microsoftonline.com/contoso.onmicrosoft.com/oauth2/v2.0/token"


async def test_authorization_server_scopes_tenant_by_auth_domain() -> None:
    hass = HomeAssistant()
    await async_set_tenant(hass, "ha_teams.client-a", "tenant-a")
    await async_set_tenant(hass, "ha_teams.client-b", "tenant-b")

    server_a = await _async_get_authorization_server(hass, "ha_teams.client-a")
    server_b = await _async_get_authorization_server(hass, "ha_teams.client-b")

    assert server_a.authorize_url == "https://login.microsoftonline.com/tenant-a/oauth2/v2.0/authorize"
    assert server_b.authorize_url == "https://login.microsoftonline.com/tenant-b/oauth2/v2.0/authorize"
