"""Unit tests for the persisted Microsoft Entra tenant store."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from custom_components.ha_teams.tenant_store import async_get_tenant, async_set_tenant


async def test_default_tenant_is_common_when_nothing_persisted() -> None:
    hass = HomeAssistant()
    assert await async_get_tenant(hass, "ha_teams.client-a") == "common"


async def test_set_tenant_persists_and_round_trips() -> None:
    hass = HomeAssistant()
    await async_set_tenant(hass, "ha_teams.client-a", "contoso.onmicrosoft.com")
    assert await async_get_tenant(hass, "ha_teams.client-a") == "contoso.onmicrosoft.com"


async def test_overwriting_tenant_replaces_previous_value_for_same_auth_domain() -> None:
    hass = HomeAssistant()
    await async_set_tenant(hass, "ha_teams.client-a", "organizations")
    await async_set_tenant(hass, "ha_teams.client-a", "consumers")
    assert await async_get_tenant(hass, "ha_teams.client-a") == "consumers"


async def test_tenants_are_isolated_per_auth_domain() -> None:
    """Multiple credentials/entries must not overwrite each other's tenants."""
    hass = HomeAssistant()
    await async_set_tenant(hass, "ha_teams.client-a", "tenant-a")
    await async_set_tenant(hass, "ha_teams.client-b", "tenant-b")

    assert await async_get_tenant(hass, "ha_teams.client-a") == "tenant-a"
    assert await async_get_tenant(hass, "ha_teams.client-b") == "tenant-b"


async def test_tenant_is_isolated_per_hass_instance() -> None:
    hass_a = HomeAssistant()
    hass_b = HomeAssistant()
    await async_set_tenant(hass_a, "ha_teams.client-a", "tenant-a")
    assert await async_get_tenant(hass_a, "ha_teams.client-a") == "tenant-a"
    assert await async_get_tenant(hass_b, "ha_teams.client-a") == "common"
