# Home Assistant – Microsoft Teams (ha-teams)

Custom Home Assistant integration that sends notifications to a Microsoft
Teams channel using the **Microsoft Graph API**, authenticated with the
**OAuth 2.0 Authorization Code flow + PKCE** (RFC 7636). No client secret
needs to be stored in Home Assistant — the app registration can be a
"public client", which is both safer and easier to configure than the
legacy Incoming Webhook / Office 365 Connector method Microsoft has
retired.

## Why PKCE instead of a client secret?

* No long-lived secret stored in `.storage/application_credentials` — only
  a short-lived access token + refresh token.
* Matches Microsoft Entra ID's recommended pattern for native/public
  clients.
* Works the same for single-tenant, multi-tenant, or personal Microsoft
  accounts (the app registration's "supported account types" controls that,
  not this integration).

## 1. Register an application in Microsoft Entra ID (Azure AD)

1. Go to [Microsoft Entra admin center](https://entra.microsoft.com/) →
   **Applications → App registrations → New registration**.
2. Name: `Home Assistant Teams` (or anything you like).
3. Supported account types: choose what fits your tenant (e.g. "Accounts
   in this organizational directory only").
4. Redirect URI: platform **Web** (not "Public client/native"), value:
   `https://my.home-assistant.io/redirect/oauth` if you use My Home
   Assistant, or `https://<your-ha-url>/auth/external/callback` otherwise.
5. After creation, go to **Authentication** and enable
   **"Allow public client flows"** → Yes. This lets the app use PKCE
   without a client secret.
6. Go to **API permissions** → **Add a permission** → **Microsoft Graph**
   → **Delegated permissions**, and add:
   - `ChannelMessage.Send`
   - `Team.ReadBasic.All`
   - `Channel.ReadBasic.All`
   - `offline_access`
   - `openid`, `profile`
   Grant admin consent if your tenant requires it.
7. Copy the **Application (client) ID** from the Overview page. You do
   **not** need a client secret.

## 2. Add Application Credentials in Home Assistant

1. In Home Assistant, go to **Settings → Devices & services →
   Application Credentials** → **Add Application Credential**.
2. Integration: `Microsoft Teams`.
3. Client ID: paste the Application (client) ID from step 1.
4. Client Secret: leave empty (PKCE is used instead); if the form
   requires a value, enter any placeholder — it is not used for the
   authorization code exchange.

## 3. Install via HACS (recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=aavdberg&repository=ha-teams&category=integration)

Click the button above, or manually:

1. Open HACS in Home Assistant.
2. Click the three dots menu (top right) and select **Custom repositories**.
3. Add `https://github.com/aavdberg/ha-teams` with category **Integration**.
4. Search for "Microsoft Teams" in HACS and click **Install**.
5. Restart Home Assistant.
6. Add the integration:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ha_teams)

## 4. Add the integration

1. **Settings → Devices & services → Add integration → Microsoft Teams.**
2. Sign in with the Microsoft account that is a member of the target Team.
3. Home Assistant lists the Teams/Channels you belong to — pick a Team,
   then a Channel. If listing fails (e.g. missing admin consent), you can
   paste the Team ID / Channel ID manually (found via *"Get link to
   channel"* in Teams).
4. Use **Options** on the integration entry any time to change the
   destination channel.

## 5. Send notifications

```yaml
action: notify.send_message
target:
  entity_id: notify.microsoft_teams
data:
  title: "Front door"
  message: "Motion detected at {{ now().strftime('%H:%M') }}"
```

## Repository layout

```
custom_components/ha_teams/
  __init__.py               # entry setup/unload, runtime data
  api.py                    # Microsoft Graph API client
  application_credentials.py# authorize/token endpoints for the OAuth2 flow
  config_flow.py            # OAuth2 (PKCE) flow + team/channel options flow
  const.py                  # domain, scopes, endpoints
  manifest.json
  notify.py                 # notify platform entity
  pkce_oauth2.py            # PKCE-enabled OAuth2 implementation
  strings.json / translations/en.json
```

## Status

Not yet in the default HACS/Home Assistant core catalogs — add it as a
custom HACS repository using the button in step 3 above, or copy
`custom_components/ha_teams` into your Home Assistant
`config/custom_components/` folder manually, then restart Home Assistant.

## License

MIT — see [LICENSE](LICENSE).
