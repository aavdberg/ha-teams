# Frequently asked questions

## Does ha-teams use an Incoming Webhook?

No. It uses the Microsoft Graph API. Microsoft has retired the legacy Office
365 Connector approach that originally motivated many Teams webhook
integrations.

## Why do messages appear under my Microsoft user name?

The current transport uses delegated Graph access and sends as the signed-in
user. A Bot Framework transport that could appear as a Home Assistant app is
planned but not implemented.

## Do I need a client secret?

No. The integration uses Authorization Code flow with PKCE and an Entra public
client. Enable **Allow public client flows** and do not create a secret for
ha-teams.

If Home Assistant requires text in the Client Secret field, use a harmless
placeholder. The integration does not submit it during token exchange.

## Why is the redirect URI configured as Web?

Home Assistant receives the OAuth callback through its web endpoint. For this
integration, configure the callback URI under the Entra **Web** platform even
though public-client flows are enabled for PKCE.

## Which tenant value should I use?

- Single-tenant app: Directory tenant ID or verified tenant domain.
- Multi-tenant organizational app: `organizations` or `common`.
- Organizational and personal accounts: `common`.
- Personal accounts only: `consumers`.

`AADSTS50194` usually means a single-tenant app was used with `common`.

## Why are admin permissions requested?

The integration requests delegated Graph scopes. Whether an administrator must
approve them depends on Microsoft Entra tenant consent policy. ha-teams cannot
bypass that policy.

## Can I send to a private or shared channel?

Support depends on Microsoft Graph, the account's membership, channel type, and
tenant policy. If the channel appears during discovery and the user is allowed
to post, test a message. If discovery does not list it, manual IDs may help but
do not bypass Microsoft authorization.

## Can I configure several channels?

Yes. Add the integration once per destination. Each config entry creates its
own notify entity and can use a different account, credential, Team, or Channel.

## Can one entry send dynamically to any channel?

No. One entry has one selected destination. This prevents automations from
passing arbitrary Team and Channel IDs. Use multiple entries and select the
appropriate entity or config entry.

## How do I find my notify entity?

Go to **Settings > Devices & services > Microsoft Teams > Entities**. The ID is
derived from the entry title and can change when renamed, so do not assume a
fixed value.

## How do I find the Adaptive Card config entry ID?

Select **Microsoft Teams: Send Adaptive Card** in the visual action editor and
choose the entry from the selector. Home Assistant writes the correct ID into
the generated YAML.

## Can Adaptive Card buttons call Home Assistant?

Not currently. Buttons requiring `Action.Submit`, `Action.Execute`, or a
callback need the planned Bot Framework transport and secure inbound request
validation. `Action.OpenUrl` can work because it is handled by the Teams client.

## Does ha-teams refresh tokens automatically?

Yes. Home Assistant's OAuth session refreshes access tokens. If refresh fails or
access is revoked, the integration raises an authentication failure so Home
Assistant can start reauthentication.

## Why is my notify entity unavailable?

The entry has no complete Team/Channel destination. Open **Configure** on the
integration entry and select or manually enter both IDs.

## Can I use a personal Microsoft account?

Only if the Entra app registration supports personal Microsoft accounts and the
account has access to the relevant Teams environment. Use `common` or
`consumers` according to the registration.

## Is ha-teams part of Home Assistant Core or the default HACS catalog?

No. It is a custom integration. Add this repository to HACS as a custom
integration repository or install it manually.

## Why is the integration icon missing?

Home Assistant 2026.3 and newer can use the included local brand images. Older
supported versions may display a placeholder without affecting operation.

## Where should I report a problem?

- Normal bugs and setup problems:
  [GitHub Issues](https://github.com/aavdberg/ha-teams/issues)
- Suspected security vulnerabilities:
  [Private Vulnerability Reporting](https://github.com/aavdberg/ha-teams/security/advisories/new)

Always redact tokens, tenant-private information, Team/Channel IDs, names,
message content, and personal data.

## What features are planned but unavailable?

- Bot Framework transport
- Sending as a Home Assistant bot/app
- Interactive card callbacks
- Microsoft Teams Activity Feed notifications
- Automated bot installation and conversation reference capture

Do not configure Azure Bot resources for the current Graph transport; they are
not used.
