# Troubleshooting

Start with the symptom below. When collecting logs or diagnostics, follow the
[security and privacy guidance](Security-and-privacy).

## Microsoft Teams is missing from Add Integration

1. Confirm `/config/custom_components/ha_teams/manifest.json` exists.
2. Confirm there is no extra nested directory.
3. Restart Home Assistant completely.
4. Check **Settings > System > Logs** for `ha_teams` import errors.
5. Confirm Home Assistant 2024.6 or newer.
6. If using HACS, confirm the repository download completed.

## Microsoft Teams is missing from Application Credentials

Install the integration and restart Home Assistant first. Application
Credentials discovers authentication providers from installed integrations.
Open it from the three-dot menu on **Settings > Devices & services**, or go
directly to `/config/application_credentials`.

## AADSTS50194 during sign-in

The app registration is single-tenant but Home Assistant is using `common`.

Use the Directory (tenant) ID or verified tenant domain from the Entra Overview
page. If needed, restart the setup flow and enter the correct tenant.

## Redirect URI mismatch

Microsoft commonly reports `AADSTS50011`.

Confirm:

- The URI is configured under platform **Web**.
- It exactly matches either the My Home Assistant redirect or your direct Home
  Assistant `/auth/external/callback` URI.
- Scheme, hostname, port, path, and trailing slash are identical.
- Home Assistant's external URL is correct.

See [Microsoft Entra app registration](Microsoft-Entra-app-registration).

## Consent required or permission denied

An administrator may need to grant consent.

Verify delegated Graph permissions:

- `ChannelMessage.Send`
- `Team.ReadBasic.All`
- `Channel.ReadBasic.All`
- `offline_access`
- `openid`
- `profile`

After changing permissions or consent, reauthenticate the integration so the
new grant is reflected in the token.

## No Teams are listed

Possible causes:

- The signed-in account has not joined any Teams.
- `Team.ReadBasic.All` consent is missing.
- Tenant policy blocks discovery.
- Microsoft Graph is temporarily unavailable.
- The wrong Microsoft account or tenant was used.

The integration offers manual Team and Channel ID entry when discovery fails.
Manual IDs do not bypass membership or send permissions.

## No channels are listed

Verify:

- The Team still exists.
- The account is a Team member.
- `Channel.ReadBasic.All` is granted.
- The account can see the channel in Microsoft Teams.

Retry **Configure**. If needed, use IDs from **Get link to channel**.

## Notify entity is unavailable

The entry does not have both a Team ID and Channel ID.

Open:

**Settings > Devices & services > Microsoft Teams > Configure**

Select or manually enter a destination. The entry reloads after saving.

## HTTP 401 or reauthentication prompt

The token is invalid, expired without a usable refresh token, or revoked.

Complete Home Assistant's reauthentication flow. If it repeats:

- Confirm the app registration still exists.
- Confirm public-client flows remain enabled.
- Confirm the account is enabled and allowed to sign in.
- Confirm consent has not been removed.
- Confirm the tenant value still matches the registration.

## HTTP 403 when sending

HTTP 403 normally indicates authorization rather than a transient outage.

Check:

- `ChannelMessage.Send` delegated consent.
- The signed-in account is a member of the Team.
- The user is allowed to post in the channel.
- The Team or channel policy has not changed.
- The target IDs still belong to the intended tenant.

Reauthenticate after permission changes.

## HTTP 404 when sending

The Team or Channel ID may be stale, deleted, or from another tenant. Open the
entry's options and select the destination again.

## HTTP 429 or Microsoft Graph 5xx

The integration retries rate limits and transient server errors up to four
attempts. For 429 responses, it respects Microsoft's `Retry-After` header.

If failures continue:

- Reduce notification bursts.
- Combine repetitive alerts.
- Check Microsoft 365 service health.
- Review Home Assistant logs for the final response status.

## Adaptive Card fails with HTTP 400

The card is malformed or uses unsupported Teams schema features.

1. Start with the minimal example on [Adaptive Cards](Adaptive-Cards).
2. Set `type: AdaptiveCard` and `version: "1.5"`.
3. Remove elements until the card succeeds.
4. Confirm YAML data types and indentation.
5. Test Teams support for the chosen card elements.

## The message appears under my name

This is expected. The current transport sends through Microsoft Graph as the
signed-in user. Sending as a Home Assistant app or bot is not implemented.

## The channel changed but automations did not

Automations target a notify entity, not a hard-coded channel. Changing entry
options keeps the same entity and redirects future messages. Confirm you edited
the same config entry used by the automation.

## Diagnostics

From the integration entry, use **Download diagnostics** when available.
ha-teams redacts:

- Access, refresh, and ID tokens
- Authentication implementation identifiers
- Team IDs
- Channel IDs

Team and Channel display names are not currently redacted. Review the file
yourself before sharing it and remove names, environment details, or other
fields that may be sensitive in your context.

## Enable debug logging temporarily

Add:

```yaml
logger:
  logs:
    custom_components.ha_teams: debug
```

Restart or reload logging as appropriate, reproduce the problem once, and then
remove or lower debug logging. Review logs for private message content,
identifiers, URLs, or Microsoft response data before posting them publicly.

## Opening an issue

Search [existing issues](https://github.com/aavdberg/ha-teams/issues) first.
Include:

- Home Assistant version
- ha-teams version
- Installation method
- Exact setup stage or action that fails
- Redacted error text and relevant logs
- Whether Team/Channel discovery works
- Whether reauthentication was attempted

Use [private vulnerability reporting](https://github.com/aavdberg/ha-teams/security/advisories/new)
for suspected security issues.
