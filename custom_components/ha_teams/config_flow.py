"""Config flow for Microsoft Teams, using Authorization Code + PKCE.

The OAuth2 login itself (including PKCE) is handled by
``AbstractOAuth2FlowHandler`` combined with the custom implementation in
``oauth.py``. Once authenticated, the entry is created immediately;
picking which Team/Channel to post to happens in the Options flow, where we
already have a working OAuth2Session backed by the real config entry.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import SOURCE_REAUTH, ConfigEntry, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client, config_entry_oauth2_flow

from .const import (
    CONF_CHANNEL_ID,
    CONF_CHANNEL_NAME,
    CONF_TEAM_ID,
    CONF_TEAM_NAME,
    CONF_TENANT_ID,
    DOMAIN,
    OAUTH2_AUTHORIZE_TEMPLATE,
    OAUTH2_TOKEN_TEMPLATE,
)
from .graph import TeamsGraphApiClient
from .tenant_store import async_get_tenant, async_set_tenant

_LOGGER = logging.getLogger(__name__)


class TeamsOAuth2FlowHandler(config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN):
    """Handle the OAuth2 Authorization Code + PKCE login flow."""

    DOMAIN = DOMAIN
    VERSION = 1

    def __init__(self) -> None:
        """Initialize the OAuth2 config flow."""
        super().__init__()
        self._tenant: str = "common"
        self._tenant_confirmed = False

    @property
    def logger(self) -> logging.Logger:
        """Return the logger used by the OAuth2 base flow."""
        return _LOGGER

    async def async_step_auth(self, user_input: dict[str, Any] | None = None) -> Any:
        """Ask for the tenant after credentials are selected, before Microsoft login."""
        if user_input is None and not self._tenant_confirmed:
            self._tenant = await async_get_tenant(self.hass, self.flow_impl.domain)
            return self.async_show_form(
                step_id="tenant",
                data_schema=vol.Schema({vol.Required(CONF_TENANT_ID, default=self._tenant): str}),
            )
        return await super().async_step_auth(user_input)

    async def async_step_tenant(self, user_input: dict[str, Any]) -> Any:
        """Persist and apply the tenant selected for this OAuth credential."""
        self._tenant = user_input[CONF_TENANT_ID].strip() or "common"
        self._tenant_confirmed = True
        await async_set_tenant(self.hass, self.flow_impl.domain, self._tenant)
        self.flow_impl.authorize_url = OAUTH2_AUTHORIZE_TEMPLATE.format(tenant=self._tenant)
        self.flow_impl.token_url = OAUTH2_TOKEN_TEMPLATE.format(tenant=self._tenant)
        return await super().async_step_auth()

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> Any:
        """Start a reauthentication flow when the refresh token is revoked.

        Triggered by ``ConfigEntryAuthFailed`` raised in ``__init__.py`` when
        token refresh fails (e.g. the user revoked consent in Entra ID).
        """
        if auth_domain := entry_data.get("auth_implementation"):
            self._tenant = await async_get_tenant(self.hass, auth_domain)
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None) -> Any:
        """Ask the user to confirm before re-running the PKCE login."""
        if user_input is None:
            return self.async_show_form(step_id="reauth_confirm")
        return await self.async_step_user()

    async def async_oauth_create_entry(self, data: dict[str, Any]) -> Any:
        """Create (or update, on reauth) the config entry after PKCE login.

        Team/channel selection is deferred to the options flow so it can
        reuse the fully-managed OAuth2Session (token refresh, storage, etc.)
        that only exists once the entry is set up.
        """
        if self.source == SOURCE_REAUTH:
            reauth_entry = self._get_reauth_entry()
            return self.async_update_reload_and_abort(reauth_entry, data=data)
        return self.async_create_entry(title="Microsoft Teams", data=data)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Return the options flow used to pick the destination channel."""
        return TeamsOptionsFlowHandler()


class TeamsOptionsFlowHandler(OptionsFlow):
    """Let the user pick which Team/Channel to send notifications to."""

    def __init__(self) -> None:
        """Initialize the options flow."""
        self._teams: list[dict[str, Any]] = []
        self._channels: list[dict[str, Any]] = []
        self._selected_team_id: str | None = None

    async def _async_get_client(self) -> TeamsGraphApiClient:
        hass = self.hass
        entry = self.config_entry
        implementation = await config_entry_oauth2_flow.async_get_config_entry_implementation(hass, entry)
        oauth_session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
        session = aiohttp_client.async_get_clientsession(hass)
        return TeamsGraphApiClient(session, oauth_session)

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> Any:
        """Fetch the joined teams and show the selection form."""
        try:
            client = await self._async_get_client()
            self._teams = await client.async_list_joined_teams()
        except Exception:
            _LOGGER.exception("Failed to list joined Teams")
            self._teams = []

        if not self._teams:
            return await self.async_step_manual_ids()

        if user_input is not None:
            self._selected_team_id = user_input[CONF_TEAM_ID]
            return await self.async_step_channel()

        options = {t["id"]: t.get("displayName", t["id"]) for t in self._teams}
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({vol.Required(CONF_TEAM_ID): vol.In(options)}),
        )

    async def async_step_channel(self, user_input: dict[str, Any] | None = None) -> Any:
        """Ask the user to pick a Channel within the selected Team."""
        assert self._selected_team_id is not None
        team = next((t for t in self._teams if t["id"] == self._selected_team_id), None)

        if user_input is not None:
            channel_id = user_input[CONF_CHANNEL_ID]
            channel = next((c for c in self._channels if c["id"] == channel_id), None)
            data = {
                CONF_TEAM_ID: self._selected_team_id,
                CONF_TEAM_NAME: team.get("displayName") if team else self._selected_team_id,
                CONF_CHANNEL_ID: channel_id,
                CONF_CHANNEL_NAME: channel.get("displayName") if channel else channel_id,
            }
            return self.async_create_entry(title="", data=data)

        try:
            client = await self._async_get_client()
            self._channels = await client.async_list_channels(self._selected_team_id)
        except Exception:
            _LOGGER.exception("Failed to list channels for team %s", self._selected_team_id)
            return await self.async_step_manual_ids()

        options = {c["id"]: c.get("displayName", c["id"]) for c in self._channels}
        return self.async_show_form(
            step_id="channel",
            data_schema=vol.Schema({vol.Required(CONF_CHANNEL_ID): vol.In(options)}),
        )

    async def async_step_manual_ids(self, user_input: dict[str, Any] | None = None) -> Any:
        """Fallback: let the user paste Team/Channel IDs manually.

        Useful when the signed-in account has no joined teams visible yet,
        or the Graph calls failed (e.g. missing admin consent for the
        tenant, or the "Team.ReadBasic.All"/"Channel.ReadBasic.All" scopes
        were not granted).
        """
        if user_input is not None:
            data = {
                CONF_TEAM_ID: user_input[CONF_TEAM_ID],
                CONF_TEAM_NAME: user_input[CONF_TEAM_ID],
                CONF_CHANNEL_ID: user_input[CONF_CHANNEL_ID],
                CONF_CHANNEL_NAME: user_input[CONF_CHANNEL_ID],
            }
            return self.async_create_entry(title="", data=data)

        return self.async_show_form(
            step_id="manual_ids",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TEAM_ID): str,
                    vol.Required(CONF_CHANNEL_ID): str,
                }
            ),
        )
