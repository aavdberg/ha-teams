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

## 2. Install via HACS (recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=aavdberg&repository=ha-teams&category=integration)

Click the button above, or manually:

1. Open HACS in Home Assistant.
2. Click the three dots menu (top right) and select **Custom repositories**.
3. Add `https://github.com/aavdberg/ha-teams` with category **Integration**.
4. Search for "Microsoft Teams" in HACS and click **Install**.
5. Restart Home Assistant.

> The integration must be installed (and Home Assistant restarted) before
> it shows up as an option in the Application Credentials picker below.

## 3. Add Application Credentials in Home Assistant

1. In Home Assistant, go to **Settings → Devices & services →
   Application Credentials** → **Add Application Credential**.
2. Integration: `Microsoft Teams`.
3. Client ID: paste the Application (client) ID from step 1.
4. Client Secret: leave empty (PKCE is used instead); if the form
   requires a value, enter any placeholder — it is not used for the
   authorization code exchange.

## 4. Add the integration

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ha_teams)

1. **Settings → Devices & services → Add integration → Microsoft Teams.**
2. **Transport**: choose **Microsoft Graph (send as signed-in user)**.
   This is the current working transport and sends channel messages as the
   Microsoft account you authenticate with. The integration stores this per
   config entry, so you can add more Microsoft Teams entries later for other
   transports or destinations.
3. **Tenant**: if your app registration is single-tenant ("Accounts in
   this organizational directory only", step 1 above), enter your
   Microsoft Entra **tenant ID** or verified domain (e.g.
   `contoso.onmicrosoft.com`) — find it on the Entra ID **Overview** page.
   Leave the default `common` if your app registration is multi-tenant or
   supports personal Microsoft accounts. Getting this wrong causes a
   `AADSTS50194` sign-in error; you can safely retry the flow to correct it.
4. Sign in with the Microsoft account that is a member of the target Team.
5. Home Assistant lists the Teams/Channels you belong to — pick a Team,
   then a Channel. If listing fails (e.g. missing admin consent), you can
   paste the Team ID / Channel ID manually (found via *"Get link to
   channel"* in Teams).
6. Use **Options** on the integration entry any time to change the
   destination channel.

### Multiple transports / entries

`ha-teams` is designed around **one transport mode per config entry**. Add
the integration multiple times if you want separate Teams destinations or,
later, different sender types side by side.

| Transport | Status | Sender shown in Teams | Notes |
|---|---|---|---|
| Microsoft Graph delegated | Supported now | The signed-in Microsoft user | Simple setup via PKCE; current default |
| Teams bot/app | Planned | A bot/app such as "Home Assistant" | Future Bot Framework transport for app-style sender and interactive cards |

Existing entries without an explicit transport are treated as **Microsoft
Graph delegated** for backwards compatibility.

### Future Teams bot/app transport setup

The **Teams bot/app** transport is not implemented yet, but the integration
is structured so it can be added later as a second transport mode. This is
the path to make messages appear as an app such as **Home Assistant**
instead of as the signed-in Microsoft user.

At a high level, a Bot Framework transport needs these pieces:

| Piece | Purpose |
|---|---|
| Azure Bot / Microsoft app registration | Gives the bot a Microsoft App ID and permission to talk to Teams |
| Teams app manifest package | Defines the Teams app name, icons, bot ID, scopes, and capabilities |
| Public callback endpoint | Lets Teams/Bot Framework deliver install events, messages, and future card actions back to Home Assistant |
| Team installation | Installs the bot/app into the target Team so it is allowed to participate |
| Conversation reference storage | Lets Home Assistant send proactive notifications to the right Team/channel later |

Suggested Azure/Teams setup when this transport is implemented:

1. In Azure Portal, create an **Azure Bot** resource or equivalent Microsoft
   Entra app registration for a Bot Framework bot.
2. Note the bot's **Microsoft App ID**.
3. Configure the bot's messaging endpoint to point to a public HTTPS URL
   that can reach Home Assistant. For local Home Assistant installations
   this normally requires a secure tunnel, reverse proxy, Nabu Casa remote
   URL, or another HTTPS endpoint that can forward requests to Home
   Assistant.
4. Enable the **Microsoft Teams** channel for the bot.
5. Create a Teams app manifest package (`manifest.json` plus two PNG icons).
   The manifest must reference the bot's Microsoft App ID and include the
   scopes where it may run, usually `team` and/or `personal`.
6. Install/upload that Teams app into the tenant or directly into the target
   Team.
7. When the bot is installed or first contacted, capture the Bot Framework
   conversation reference (service URL, conversation ID, tenant ID, team ID,
   and channel ID). Home Assistant needs that stored reference for
   proactive notifications.

What `ha-teams` already has prepared:

- A per-entry `transport` value, so Graph delegated and future bot entries
  can live side by side.
- Placeholder modules under `custom_components/ha_teams/bot/` for a future
  Bot Connector client, inbound callback handling, and request validation.
- Adaptive Card rendering helpers that can be reused by a future bot
  sender.

What is still future work:

- Bot Framework authentication and token handling.
- A Home Assistant webhook endpoint for Bot Framework callbacks.
- Teams app manifest generation or documentation with exact IDs.
- Conversation reference capture/storage.
- A real `teams_bot` sender implementation and UI option.

Until those pieces are implemented, use **Microsoft Graph (send as signed-in
user)**. It is the only currently selectable transport and requires much
less Azure setup.

## 5. Send notifications

After setup, Home Assistant creates a notify entity for the selected Teams
channel. The entity ID is derived from the integration entry title and can
be different if you renamed the entry or added multiple Teams entries. Check
**Settings → Devices & services → Microsoft Teams → Entities** or
**Developer Tools → States** for the exact entity ID, then replace
`notify.your_microsoft_teams_entity` in the examples below.

Before sending a test message, make sure the integration entry has a
destination configured: open **Settings → Devices & services → Microsoft
Teams → Configure** and select the target Team and Channel. Without this,
Home Assistant cannot know where to post the message.

### Basic notification

```yaml
action: notify.send_message
target:
  entity_id: notify.your_microsoft_teams_entity
data:
  title: "Front door"
  message: "Motion detected at {{ now().strftime('%H:%M') }}"
```

### Automation: send a Teams message when a sensor changes

```yaml
alias: Notify Teams when motion is detected
description: Send a Microsoft Teams notification when motion starts.
triggers:
  - trigger: state
    entity_id: binary_sensor.front_door_motion
    from: "off"
    to: "on"
actions:
  - action: notify.send_message
    target:
      entity_id: notify.your_microsoft_teams_entity
    data:
      title: "Front door"
      message: "Motion detected at {{ now().strftime('%H:%M') }}."
mode: single
```

### Automation: include entity state in the message

```yaml
alias: Notify Teams about low battery
description: Send a Teams notification when a battery sensor is low.
triggers:
  - trigger: numeric_state
    entity_id: sensor.device_battery
    below: 20
actions:
  - action: notify.send_message
    target:
      entity_id: notify.your_microsoft_teams_entity
    data:
      title: "Low battery"
      message: >-
        {{ state_attr('sensor.device_battery', 'friendly_name') or 'Device' }}
        battery is {{ states('sensor.device_battery') }}%.
mode: single
```

### Automation: multi-line status message

```yaml
alias: Notify Teams when alarm is triggered
description: Send a high-priority status message to Teams.
triggers:
  - trigger: state
    entity_id: alarm_control_panel.home_alarm
    to: "triggered"
actions:
  - action: notify.send_message
    target:
      entity_id: notify.your_microsoft_teams_entity
    data:
      title: "Alarm triggered"
      message: |
        Home Assistant alarm state changed to triggered.

        Time: {{ now().strftime('%Y-%m-%d %H:%M:%S') }}
        Mode: {{ states('alarm_control_panel.home_alarm') }}
mode: single
```

For multiple Teams entries, use the notify entity that belongs to the target
Team/channel. Each entry can point to a different destination.

## Testing the Dev Branch

> **Note:** HACS 2.x no longer supports branch selection in the UI. Use one of the methods below to test the `dev` branch.

### Option A — Manual copy (quickest)

1. In Home Assistant, open **File Editor** or connect via **SSH / Samba**
2. Copy the folder `custom_components/ha_teams` from the `dev` branch to:
   ```
   /config/custom_components/ha_teams/
   ```
3. Restart Home Assistant

To download the dev branch as a zip:
```
https://github.com/aavdberg/ha-teams/archive/refs/heads/dev.zip
```
Extract and copy the `custom_components/ha_teams` folder.

### Option B — HACS beta release (recommended for ongoing testing)

Every push to `dev` automatically creates a **pre-release** tag (e.g. `v0.2.0-beta.1`).

1. In HACS, open the **Microsoft Teams** repository
2. Select the **⋮ menu → Show details**
3. Enable **"Show beta releases"** in your HACS settings (⋮ → Settings → Experimental)
4. The latest dev pre-release will appear as an available update in HACS

### Option C — Git clone via SSH

```bash
cd /config/custom_components
git clone -b dev https://github.com/aavdberg/ha-teams.git ha_teams_dev
# Then symlink or copy the inner folder:
cp -r ha_teams_dev/custom_components/ha_teams ./ha_teams
```

## Repository layout

```
custom_components/ha_teams/
  __init__.py               # entry setup/unload, runtime data, ha_teams.send_card service
  models.py                 # TeamsRuntimeData / TeamsConfigEntry dataclasses
  application_credentials.py# authorize/token endpoints for the OAuth2 flow
  config_flow.py            # OAuth2 (PKCE) flow + reauth + team/channel options flow
  const.py                  # domain, scopes, endpoints, retry tuning
  diagnostics.py            # redacted diagnostics (tokens, team/channel IDs)
  coordinator.py            # placeholder for a future polling coordinator (not used yet)
  repairs.py                # placeholder for future repair issues (not used yet)
  manifest.json
  notify.py                 # notify platform entity
  oauth.py                  # PKCE-enabled OAuth2 implementation
  services.yaml             # ha_teams.send_card service definition
  strings.json / translations/en.json
  brand/                     # icon.png, icon@2x.png, logo.png, logo@2x.png (local brand images)

  graph/                     # Microsoft Graph API client
    __init__.py               # composes TeamsGraphApiClient from the mixins below
    client.py                  # HTTP transport: retry/backoff, GraphApiError/GraphAuthError
    discovery.py                # list joined Teams / Channels
    messages.py                  # send channel message / Adaptive Card
    activity.py                   # placeholder: future "activity feed" notifications
    app_installation.py            # placeholder: future app/bot installation for a team

  renderers/                  # turn HA notification data into Graph payloads
    __init__.py
    text.py                     # plain-text (title + message -> Markdown)
    adaptive_card.py              # Adaptive Card chatMessage payload builder
    activity.py                    # placeholder: future activity-feed payload renderer

  bot/                        # placeholder: future Bot Framework transport (interactive cards)
    __init__.py
    client.py                    # placeholder: Bot Connector REST client
    callbacks.py                  # placeholder: inbound card-action webhook handler
    validation.py                  # placeholder: inbound request/signature validation

tests/                       # pytest unit tests (mirrors the package layout above)
```

The `graph/`, `renderers/`, and `bot/` placeholder modules exist now so the
integration can grow into features deliberately deferred for now — a Bot
Framework transport (interactive Adaptive Card actions) and Graph Activity
Feed notifications — without another restructuring pass later. See
[`.github/copilot-instructions.md`](.github/copilot-instructions.md) for
what's deferred and why.

## Status

Not yet in the default HACS/Home Assistant core catalogs — add it as a
custom HACS repository using the button in step 3 above, or copy
`custom_components/ha_teams` into your Home Assistant
`config/custom_components/` folder manually, then restart Home Assistant.

The integration ships its own Microsoft Teams brand icon/logo in
`custom_components/ha_teams/brand/`. Home Assistant **2026.3 and newer**
picks these up automatically (no extra configuration, no external
`home-assistant/brands` submission needed) so the integration shows the
Teams icon instead of a placeholder when adding it under **Devices &
Services**. On older Home Assistant releases the placeholder icon is
shown until this integration is submitted to the
[`home-assistant/brands`](https://github.com/home-assistant/brands)
repository.

## License

MIT — see [LICENSE](LICENSE).

---

## Development

### Branching Strategy

```
feature/* or fix/*
        │
        ▼  Pull Request + lint check
       dev         ← development & testing
        │
        ▼  Pull Request + lint check
      main         ← production (HACS users)
                      → automatic GitHub Release
```

| Branch | Purpose | Protected |
|---|---|---|
| `main` | Stable production release | ✅ PR required + lint must pass |
| `dev` | Integration & testing | ✅ PR required + lint must pass |
| `feature/*` | New functionality | Free — PR to `dev` |
| `fix/*` | Bug fixes | Free — PR to `dev` |
| `chore/*` | Non-code changes (docs, CI, repo tooling) | Free — PR to `dev` (or direct to `main` if unrelated to integration) |

### Contributing

1. Branch off `dev`:
   ```bash
   git checkout dev
   git checkout -b feature/my-feature
   ```
2. Commit your changes:
   ```bash
   git commit -m "feat: description of the change"
   ```
3. Push and open a **Pull Request to `dev`**:
   ```bash
   git push origin feature/my-feature
   ```
4. CI (ruff lint/format, pytest, HACS validation, hassfest, gitleaks) and the
   Copilot code review run automatically.
5. When `dev` is stable, a PR to `main` is opened to trigger a release.

### Releases

Every merge to `main` automatically creates a GitHub Release based on the
`version` field in `manifest.json`. Every push to `dev` creates a beta
pre-release tag (`v<version>-beta.<N>`) for HACS beta testers.
Bump the version in `manifest.json` on `dev` before opening a release PR.

### Local Development

```bash
# Install dev/test dependencies
pip install ruff -r requirements_test.txt

# Check for lint errors
ruff check custom_components/

# Check formatting
ruff format --check custom_components/

# Auto-fix issues
ruff check --fix custom_components/

# Run the unit test suite
pytest -v
```

See [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for
the full mandatory workflow (plan → issue → branch → PR → CI → review →
merge → release).
