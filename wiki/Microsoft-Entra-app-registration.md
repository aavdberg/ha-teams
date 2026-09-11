# Microsoft Entra app registration

This page creates the Microsoft identity application used by Home Assistant.
The integration uses Authorization Code flow with PKCE and does not require a
client secret.

## 1. Determine the Home Assistant redirect URI

Choose one redirect URI and use the exact same value in Microsoft Entra:

### My Home Assistant redirect

Use this when My Home Assistant is available:

```text
https://my.home-assistant.io/redirect/oauth
```

### Direct Home Assistant redirect

Use your externally reachable Home Assistant base URL:

```text
https://homeassistant.example.com/auth/external/callback
```

Replace the example host with your actual Home Assistant URL. Do not add an
extra slash. The scheme, host, port, and path must match what Home Assistant
uses.

## 2. Create the app registration

1. Open the [Microsoft Entra admin center](https://entra.microsoft.com/).
2. Go to **Identity > Applications > App registrations**.
3. Select **New registration**.
4. Enter a recognizable name, such as `Home Assistant Teams`.
5. Select the supported account type that matches your deployment.
6. Under **Redirect URI**, choose platform **Web**.
7. Enter the redirect URI selected above.
8. Select **Register**.

Although this app uses public-client flows, the redirect URI used by Home
Assistant must be configured under the **Web** platform.

## 3. Record the identifiers

On the app registration **Overview** page, record:

- **Application (client) ID**: entered in Home Assistant Application
  Credentials.
- **Directory (tenant) ID**: used as the Home Assistant tenant value for a
  single-tenant app.

These identifiers are not passwords, but they are tenant-specific information.
Use placeholders when posting screenshots or logs publicly.

## 4. Enable public-client flows

1. Open **Authentication** for the app registration.
2. Find **Advanced settings**.
3. Set **Allow public client flows** to **Yes**.
4. Save the change.

Do not create a client secret for ha-teams. PKCE protects the authorization
code exchange without requiring Home Assistant to store a long-lived secret.

## 5. Add delegated Microsoft Graph permissions

Open **API permissions**, select **Add a permission**, choose
**Microsoft Graph**, and then **Delegated permissions**.

Add these permissions:

| Permission | Why it is needed |
| --- | --- |
| `ChannelMessage.Send` | Send messages to the configured Teams channel as the signed-in user |
| `Team.ReadBasic.All` | List Teams that the signed-in user has joined |
| `Channel.ReadBasic.All` | List channels in the selected Team |
| `offline_access` | Obtain a refresh token so Home Assistant can keep working without repeated sign-in |
| `openid` | Perform OpenID Connect sign-in |
| `profile` | Read basic signed-in profile information required by the OAuth flow |

The integration requests delegated permissions only. Do not substitute
application permissions.

## 6. Grant consent

Some tenants allow users to consent during sign-in. Other organizations require
an administrator to select **Grant admin consent** on the API permissions page.

If Team or Channel discovery fails, verify that the effective consent includes
`Team.ReadBasic.All` and `Channel.ReadBasic.All`. If sending fails with HTTP
403, verify `ChannelMessage.Send`, membership, and channel policy.

## 7. Choose the tenant value

During Home Assistant setup, the integration asks for a tenant:

- Single-tenant registration: use the Directory (tenant) ID or a verified
  domain such as `contoso.onmicrosoft.com`.
- Multi-tenant registration: use `common` or `organizations`.
- Personal-account-only registration: use `consumers`.

Using `common` with a single-tenant registration commonly causes
`AADSTS50194`.

## Redirect URI checklist

If Microsoft reports a redirect mismatch:

- Confirm the Entra platform is **Web**.
- Compare the full URI character by character.
- Confirm `http` versus `https`.
- Confirm the hostname and non-default port.
- Remove an accidental trailing slash.
- Make sure Home Assistant is using the same external URL.

Next: [Install ha-teams](Installation), then
[configure Home Assistant](Home-Assistant-configuration).
