# Prerequisites and supported environments

Use this checklist before registering an application or installing the
integration.

## Home Assistant

- Home Assistant **2024.6 or newer**.
- Administrator access to install a custom integration and add Application
  Credentials.
- A working Home Assistant URL for the OAuth callback.
- HACS is recommended but not required.

Home Assistant 2026.3 and newer can display the brand images included with the
integration. Older supported Home Assistant releases may show a placeholder
icon; this does not affect functionality.

## Microsoft 365 and Teams

You need:

- A Microsoft account that can sign in to the selected tenant.
- Membership of the target Microsoft Team.
- Access to the target channel.
- Permission to send channel messages as that user.

The integration uses delegated Microsoft Graph permissions. It does not use
application-only access and does not silently post as an organization-wide
service identity.

Tenant policy can prevent users from granting consent. In that case, a
Microsoft Entra administrator must approve the requested delegated
permissions.

## Microsoft Entra access

Someone must be able to create an app registration in the relevant Microsoft
Entra tenant. Depending on organization policy, this may require an
administrator.

The app registration must allow public-client flows and must have the correct
redirect URI. Follow
[Microsoft Entra app registration](Microsoft-Entra-app-registration) exactly;
OAuth callback settings are sensitive to small differences.

## Network requirements

Home Assistant must be able to make outbound HTTPS requests to:

- `login.microsoftonline.com`
- `graph.microsoft.com`
- GitHub and HACS endpoints when installing or updating through HACS

The Graph transport does **not** require an inbound public webhook endpoint.
The browser must be able to return to the configured Home Assistant OAuth
callback after Microsoft sign-in.

## Supported account types

The supported account type is controlled by your app registration:

| Entra app registration | Tenant value in Home Assistant |
| --- | --- |
| Accounts in this organizational directory only | Your tenant ID or verified tenant domain |
| Accounts in any organizational directory | `organizations` or `common` |
| Organizational and personal Microsoft accounts | `common` |
| Personal Microsoft accounts only | `consumers` |

For the simplest organization-only deployment, use a single-tenant
registration and enter its tenant ID during Home Assistant setup.

## Current feature support

| Capability | Status |
| --- | --- |
| Plain channel messages | Supported |
| Adaptive Cards | Supported |
| Multiple config entries and destinations | Supported |
| Automatic token refresh | Supported |
| Reauthentication after revoked access | Supported |
| Sending as the signed-in user | Supported |
| Sending as a Home Assistant bot/app | Not implemented |
| Interactive card callbacks | Not implemented |
| Teams Activity Feed notifications | Not implemented |
| Incoming Webhook / Office 365 Connector transport | Not used |

Continue with [Microsoft Entra app registration](Microsoft-Entra-app-registration).
