# Home Assistant configuration

Complete the [Microsoft Entra app registration](Microsoft-Entra-app-registration)
and [installation](Installation) before following this page.

## 1. Add Application Credentials

1. Go to **Settings > Devices & services**.
2. Open the three-dot menu and select **Application Credentials**. You can
   also open `/config/application_credentials` on your Home Assistant instance.
3. Select **Add Application Credential**.
4. Choose **Microsoft Teams**.
5. Enter the Application (client) ID from the Entra app registration.
6. Enter a harmless placeholder such as `not-used` in **Client Secret** if the
   form requires a value.

ha-teams does not send the Client Secret field during the token exchange.
Never enter an unrelated real secret.

One Application Credential represents one Entra app registration. The selected
tenant is stored for that authentication implementation, so use separate
credentials when app registrations require different tenants.

## 2. Add the integration

Use the setup button:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ha_teams)

Or:

1. Go to **Settings > Devices & services**.
2. Select **Add integration**.
3. Search for **Microsoft Teams**.

## 3. Select the transport

Choose **Microsoft Graph (send as signed-in user)**.

This is the only supported transport. Messages appear in Teams as the account
used during Microsoft sign-in. Bot/app sending is planned but not implemented.

## 4. Select Application Credentials and tenant

Choose the Application Credential created above.

Enter:

- Your tenant ID or verified domain for a single-tenant registration.
- `common` for an app supporting organizations and personal accounts.
- `organizations` for organizational accounts only.
- `consumers` for personal Microsoft accounts only.

The tenant value controls both Microsoft authorization and token endpoints.

## 5. Sign in to Microsoft

Home Assistant opens Microsoft sign-in:

1. Sign in with the account that belongs to the target Team.
2. Review the requested delegated permissions.
3. Complete consent if permitted.
4. Return to Home Assistant through the OAuth redirect.

Do not sign in with a service account unless its licensing, security controls,
Team membership, and lifecycle are managed appropriately.

## 6. Select a Team and Channel

After authentication, the config entry is created. Open **Configure** on the
entry to select its destination.

1. Select a Team from the Teams joined by the signed-in user.
2. Select a Channel in that Team.
3. Save the options.

The notify entity is unavailable until both destination values are configured.

## Manual Team and Channel IDs

If discovery fails, the integration opens a manual form.

In Microsoft Teams:

1. Open the target channel.
2. Open the channel's three-dot menu.
3. Select **Get link to channel**.
4. Copy the Team ID and Channel ID contained in the URL.
5. Paste them into Home Assistant.

The IDs can be URL-encoded. Preserve the complete ID and do not replace or
remove characters unless you are deliberately URL-decoding it. Treat these IDs
as tenant-private data when sharing diagnostics or screenshots.

Manual entry bypasses discovery only; the signed-in user still needs permission
to send to that destination.

## Change the destination

1. Go to **Settings > Devices & services > Microsoft Teams**.
2. Select **Configure** on the desired entry.
3. Choose a new Team and Channel.
4. Save.

Home Assistant reloads the entry automatically. Existing automations keep using
the same notify entity and begin sending to the new destination.

## Reauthentication

Home Assistant starts a reauthentication flow when token refresh fails or
Microsoft Graph returns an authentication/permission error.

1. Open the repair or reauthentication prompt.
2. Confirm reauthentication.
3. Verify the transport and tenant.
4. Sign in again and grant required consent.

Reauthentication updates the OAuth data without requiring you to recreate the
destination options.

## Find the created entities

Open:

**Settings > Devices & services > Microsoft Teams > Entities**

The notify entity ID depends on the config entry title and any user rename. Do
not assume a fixed name. Use the exact entity ID shown by Home Assistant in
[notification examples](Sending-notifications).
