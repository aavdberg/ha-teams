# Microsoft Teams for Home Assistant

Welcome to the user guide for **ha-teams**, a Home Assistant custom
integration that sends notifications to Microsoft Teams channels through the
Microsoft Graph API.

The integration uses OAuth 2.0 Authorization Code flow with PKCE. Messages are
sent as the Microsoft user who signs in during setup. No Microsoft client
secret is required or used.

## What you can do

- Send plain-text Teams channel messages from Home Assistant automations.
- Include a title and Home Assistant templates in notifications.
- Send rich Adaptive Cards with `ha_teams.send_card`.
- Configure multiple integration entries for different channels or accounts.
- Change the destination Team and Channel without recreating the integration.
- Reauthenticate from Home Assistant if Microsoft consent or tokens are
  revoked.

## Current limitations

- Only **Microsoft Graph delegated** transport is available.
- Messages appear as the signed-in Microsoft user, not as a Home Assistant bot.
- Each config entry has one configured Team and Channel.
- Interactive Adaptive Card callbacks such as acknowledge or snooze are not
  implemented.
- Microsoft Teams Activity Feed notifications are not implemented.

## Quick start

1. Review the [prerequisites](Prerequisites-and-supported-environments.md).
2. [Register an application in Microsoft Entra](Microsoft-Entra-app-registration.md).
3. [Install ha-teams](Installation.md).
4. [Add Application Credentials and configure the integration](Home-Assistant-configuration.md).
5. [Send a test notification](Sending-notifications.md).

Most setup problems are caused by an incorrect redirect URI, tenant value, or
missing Microsoft Graph consent. See [Troubleshooting](Troubleshooting.md) for a
symptom-based guide.

## Documentation

| Topic | Use it when |
| --- | --- |
| [Prerequisites and supported environments](Prerequisites-and-supported-environments.md) | Checking whether your Home Assistant and Microsoft setup are suitable |
| [Microsoft Entra app registration](Microsoft-Entra-app-registration.md) | Creating the OAuth application and assigning Graph permissions |
| [Installation](Installation.md) | Installing with HACS or manually |
| [Home Assistant configuration](Home-Assistant-configuration.md) | Adding credentials, signing in, and choosing a channel |
| [Sending notifications](Sending-notifications.md) | Testing the notify entity and creating automations |
| [Adaptive Cards](Adaptive-Cards.md) | Sending structured cards through the integration service |
| [Multiple destinations](Multiple-destinations.md) | Sending to several channels or using several accounts |
| [Troubleshooting](Troubleshooting.md) | Resolving authentication, discovery, and delivery errors |
| [Updating and beta testing](Updating-and-beta-testing.md) | Updating, testing pre-releases, rolling back, or removing the integration |
| [Security and privacy](Security-and-privacy.md) | Understanding tokens, stored data, diagnostics, and safe reporting |
| [FAQ](FAQ.md) | Answers about bots, secrets, permissions, and limitations |

## Getting help

For normal bugs and setup problems, search the
[issue tracker](https://github.com/aavdberg/ha-teams/issues) before opening a
new issue. Remove tokens, tenant-private values, Team and Channel IDs, user
names, and message content from logs or screenshots.

Suspected vulnerabilities must be reported through
[GitHub Private Vulnerability Reporting](https://github.com/aavdberg/ha-teams/security/advisories/new),
not through a public issue.
