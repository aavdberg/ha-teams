# Security and privacy

ha-teams connects Home Assistant to Microsoft Teams through Microsoft identity
and Microsoft Graph. Treat Home Assistant, the Entra app registration, and the
signed-in account as parts of one security boundary.

## Authentication model

The integration uses OAuth 2.0 Authorization Code flow with PKCE:

- A new PKCE verifier and challenge protect each authorization attempt.
- No Microsoft client secret is required or used.
- Home Assistant stores OAuth token data so it can send notifications later.
- `offline_access` allows token refresh without repeated interactive sign-in.
- Microsoft Graph messages are sent as the signed-in user.

The absence of a client secret does not make token storage unimportant. Anyone
who obtains a valid token may be able to act with its granted permissions until
it expires or is revoked.

## Requested permissions

| Scope | Purpose |
| --- | --- |
| `ChannelMessage.Send` | Send messages to a channel as the signed-in user |
| `Team.ReadBasic.All` | Discover Teams joined by the user |
| `Channel.ReadBasic.All` | Discover channels in the selected Team |
| `offline_access` | Refresh access without repeated sign-in |
| `openid` and `profile` | Complete sign-in and identify the authenticated profile |

Do not add broader permissions unless a future feature has a documented need.

## Protect Home Assistant

- Keep Home Assistant and ha-teams updated.
- Restrict administrator access.
- Use HTTPS for remote access.
- Protect backups because they may contain Home Assistant `.storage` data.
- Do not expose `.storage` or config files through public web servers.
- Use a Microsoft account with only the access needed for intended channels.
- Remove unused config entries, Application Credentials, consent grants, and
  app registrations.

## Stored and configured data

The config entry and Application Credentials may include:

- OAuth token data managed by Home Assistant
- Authentication implementation metadata
- Tenant selection
- Transport selection
- Team and Channel destination IDs and names

Do not manually copy `.storage` files into bug reports.

## Diagnostics

ha-teams redacts access tokens, refresh tokens, ID tokens, authentication
implementation identifiers, Team IDs, and Channel IDs from its diagnostics.
Team and Channel display names are not currently redacted and must be reviewed
manually.

Redaction is a safety layer, not a substitute for review. Before sharing:

1. Open the diagnostics file.
2. Search for names, email addresses, hostnames, tenant details, message
   content, URLs, and identifiers.
3. Remove anything not needed to reproduce the problem.

## Safe notifications and cards

Teams channels can have broad membership and retention policies. Avoid sending:

- Passwords, tokens, client secrets, alarm codes, or recovery codes
- Sensitive personal or health information
- Private camera links or signed storage URLs
- Internal URLs containing credentials
- More device or household detail than recipients need

Adaptive Cards can contain links and dynamic values. Treat templated card data
as information disclosed to every user who can read the destination channel.

## Revoke access

If access may be compromised:

1. Disable or remove the ha-teams config entry.
2. Revoke the user's consent or sessions in Microsoft Entra.
3. Remove or disable the affected account when appropriate.
4. Rotate any unrelated credentials accidentally exposed in messages or logs.
5. Reauthenticate only after the cause has been addressed.

Removing a config entry from Home Assistant does not necessarily revoke an
already granted Microsoft consent. Manage both sides.

## Sharing logs and screenshots

Redact:

- OAuth access, refresh, and ID tokens
- Authorization codes
- Home Assistant access tokens
- Client secrets and credentials
- Tenant, Team, Channel, user, and message IDs
- Email addresses, names, message contents, and private URLs

Use artificial placeholders such as:

```text
TENANT_ID_REDACTED
TEAM_ID_REDACTED
CHANNEL_ID_REDACTED
notify.example_teams
```

## Report a vulnerability

Do not open a public issue for a suspected vulnerability. Use
[GitHub Private Vulnerability Reporting](https://github.com/aavdberg/ha-teams/security/advisories/new).

Read the repository
[Security Policy](https://github.com/aavdberg/ha-teams/security/policy) for
scope, safe-testing expectations, and disclosure guidance.
