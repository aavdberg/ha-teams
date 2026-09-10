"""Persist Microsoft Entra tenants per Home Assistant OAuth credential.

Most Microsoft Entra ID (Azure AD) app registrations default to "Accounts
in this organizational directory only" (single-tenant). Microsoft only
allows such apps to authenticate against their own tenant-specific
endpoint (``https://login.microsoftonline.com/<tenant>/...``) -- using the
multi-tenant ``/common`` endpoint fails with ``AADSTS50194``. The config
flow asks the user for their tenant once (defaulting to "common" for
multi-tenant/personal-account app registrations). It is persisted per
``auth_implementation`` (Home Assistant's application-credential ID) so
multiple Teams config entries can use different Entra tenants without
overwriting each other's token-refresh endpoint.
"""

from __future__ import annotations

from asyncio import Lock

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DEFAULT_TENANT, DOMAIN

_STORAGE_VERSION = 1
_STORAGE_KEY = f"{DOMAIN}.tenant"
_LOCK_ATTR = "_ha_teams_tenant_store_lock"


def _store(hass: HomeAssistant) -> Store:
    return Store(hass, _STORAGE_VERSION, _STORAGE_KEY)


def _lock(hass: HomeAssistant) -> Lock:
    lock = getattr(hass, _LOCK_ATTR, None)
    if lock is None:
        lock = Lock()
        setattr(hass, _LOCK_ATTR, lock)
    return lock


async def _async_load_tenants(hass: HomeAssistant) -> dict[str, str]:
    """Return persisted tenants keyed by auth implementation id."""
    data = await _store(hass).async_load()
    if not data:
        return {}
    return data.get("tenants", {})


async def async_get_tenant(hass: HomeAssistant, auth_domain: str) -> str:
    """Return the Microsoft Entra tenant for an auth implementation."""
    tenants = await _async_load_tenants(hass)
    return tenants.get(auth_domain, DEFAULT_TENANT)


async def async_set_tenant(hass: HomeAssistant, auth_domain: str, tenant: str) -> None:
    """Persist the tenant used by one Home Assistant OAuth credential."""
    async with _lock(hass):
        tenants = await _async_load_tenants(hass)
        await _store(hass).async_save({"tenants": {**tenants, auth_domain: tenant}})
