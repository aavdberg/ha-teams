"""Pytest fixtures + lightweight stubs for homeassistant modules.

We deliberately avoid depending on the full ``homeassistant`` core package
(a heavy dependency) for these unit tests. Instead we stub out the small
surface area that ``custom_components/ha_teams`` imports at module load
time, so the real integration modules can be imported and their pure logic
(PKCE math, retry classification, Adaptive Card payload building) exercised
directly and fast, inside the WSL test container.
"""

from __future__ import annotations

import sys
import types

import pytest


def _ensure_module(name: str) -> types.ModuleType:
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    sys.modules[name] = module
    return module


def _install_homeassistant_stubs() -> None:
    """Install minimal stand-ins for the homeassistant.* modules we import."""
    ha = _ensure_module("homeassistant")
    ha.__path__ = []  # mark as a package

    core = _ensure_module("homeassistant.core")

    class HomeAssistant:
        """Stand-in for homeassistant.core.HomeAssistant."""

    class ServiceCall:
        """Stand-in for homeassistant.core.ServiceCall."""

        def __init__(self, data: dict | None = None) -> None:
            self.data = data or {}

    def callback(func):
        return func

    core.HomeAssistant = HomeAssistant
    core.ServiceCall = ServiceCall
    core.callback = callback

    config_entries = _ensure_module("homeassistant.config_entries")

    class ConfigEntry:
        """Stand-in for homeassistant.config_entries.ConfigEntry."""

    class OptionsFlow:
        """Stand-in for homeassistant.config_entries.OptionsFlow."""

    config_entries.ConfigEntry = ConfigEntry
    config_entries.OptionsFlow = OptionsFlow
    config_entries.SOURCE_REAUTH = "reauth"

    const = _ensure_module("homeassistant.const")

    class Platform:
        NOTIFY = "notify"

    const.Platform = Platform

    exceptions = _ensure_module("homeassistant.exceptions")

    class ConfigEntryAuthFailed(Exception):
        """Stand-in for homeassistant.exceptions.ConfigEntryAuthFailed."""

    class ServiceValidationError(Exception):
        """Stand-in for homeassistant.exceptions.ServiceValidationError."""

    exceptions.ConfigEntryAuthFailed = ConfigEntryAuthFailed
    exceptions.ServiceValidationError = ServiceValidationError

    helpers = _ensure_module("homeassistant.helpers")
    helpers.__path__ = []

    aiohttp_client = _ensure_module("homeassistant.helpers.aiohttp_client")

    def async_get_clientsession(hass):
        raise NotImplementedError("stub not used in unit tests")

    aiohttp_client.async_get_clientsession = async_get_clientsession

    oauth2_flow = _ensure_module("homeassistant.helpers.config_entry_oauth2_flow")

    class OAuth2Session:
        def __init__(self, hass=None, entry=None, implementation=None) -> None:
            self.hass = hass
            self.entry = entry
            self.implementation = implementation
            self.token: dict = {"access_token": "stub-token"}

        async def async_ensure_token_valid(self) -> None:
            return None

    class LocalOAuth2Implementation:
        def __init__(self, hass, domain, client_id, client_secret, authorize_url, token_url):
            self.hass = hass
            self.domain = domain
            self.client_id = client_id
            self.client_secret = client_secret
            self.authorize_url = authorize_url
            self.token_url = token_url

        async def _token_request(self, data: dict) -> dict:
            return {}

    class AbstractOAuth2FlowHandler:
        def __init_subclass__(cls, domain: str | None = None, **kwargs) -> None:
            super().__init_subclass__(**kwargs)
            cls._domain = domain

    async def async_get_config_entry_implementation(hass, entry):
        raise NotImplementedError("stub not used in unit tests")

    oauth2_flow.OAuth2Session = OAuth2Session
    oauth2_flow.LocalOAuth2Implementation = LocalOAuth2Implementation
    oauth2_flow.AbstractOAuth2FlowHandler = AbstractOAuth2FlowHandler
    oauth2_flow.async_get_config_entry_implementation = async_get_config_entry_implementation

    app_credentials = _ensure_module("homeassistant.components.application_credentials")

    class ClientCredential:
        def __init__(self, client_id: str, client_secret: str | None = None) -> None:
            self.client_id = client_id
            self.client_secret = client_secret

    class AuthorizationServer:
        def __init__(self, authorize_url: str, token_url: str) -> None:
            self.authorize_url = authorize_url
            self.token_url = token_url

    class AuthImplementation(LocalOAuth2Implementation):
        pass

    app_credentials.ClientCredential = ClientCredential
    app_credentials.AuthorizationServer = AuthorizationServer
    app_credentials.AuthImplementation = AuthImplementation

    diagnostics = _ensure_module("homeassistant.components.diagnostics")

    def async_redact_data(data, to_redact):
        return {k: ("**REDACTED**" if k in to_redact else v) for k, v in data.items()}

    diagnostics.async_redact_data = async_redact_data

    components = _ensure_module("homeassistant.components")
    components.__path__ = []

    notify = _ensure_module("homeassistant.components.notify")

    class NotifyEntity:
        pass

    class NotifyEntityDescription:
        def __init__(self, key: str, name=None) -> None:
            self.key = key
            self.name = name

    notify.NotifyEntity = NotifyEntity
    notify.NotifyEntityDescription = NotifyEntityDescription

    entity_platform = _ensure_module("homeassistant.helpers.entity_platform")

    class AddEntitiesCallback:
        pass

    entity_platform.AddEntitiesCallback = AddEntitiesCallback


_install_homeassistant_stubs()


@pytest.fixture(autouse=True)
def _reinstall_stubs():
    """Keep stubs installed even if a test module reload clears sys.modules."""
    _install_homeassistant_stubs()
    yield
