# Multiple destinations

Each ha-teams config entry has one transport and one configured Team/Channel
destination. Add multiple entries when automations need to send to different
channels or Microsoft accounts.

## Example layout

| Config entry | Signed-in account | Destination | Notify entity |
| --- | --- | --- | --- |
| Operations | operations user | Operations / Alerts | `notify.teams_operations` |
| Household | household user | Home / Notifications | `notify.teams_household` |
| Testing | test user | Lab / Home Assistant | `notify.teams_testing` |

Entity IDs are examples only. Use the IDs shown by your Home Assistant instance.

## Add another destination

1. Confirm the Microsoft account is a member of the target Team.
2. Add the Microsoft Teams integration again.
3. Select the appropriate Application Credential and tenant.
4. Sign in with the desired Microsoft account.
5. Open **Configure** on the new entry.
6. Select its Team and Channel.
7. Rename the config entry to a descriptive name if needed.

Home Assistant creates a separate notify entity and device for every entry.

## Use different entries in automations

Plain notifications target the desired notify entity:

```yaml
actions:
  - action: notify.send_message
    target:
      entity_id: notify.teams_operations
    data:
      title: "System alert"
      message: "The backup failed."
```

Adaptive Cards select the desired config entry:

```yaml
actions:
  - action: ha_teams.send_card
    data:
      config_entry_id: 0123456789abcdef0123456789abcdef
      card:
        type: AdaptiveCard
        version: "1.5"
        body:
          - type: TextBlock
            text: Test environment status
            wrap: true
```

Use the visual action editor to avoid mixing up config entry IDs.

## Shared versus separate app registrations

Multiple entries can reuse one Home Assistant Application Credential when they
use the same Entra app registration and tenant.

Use separate Application Credentials when:

- Entries belong to different Entra tenants.
- Different app registrations are required by organization policy.
- You need separate consent or lifecycle management.

The tenant value is associated with the authentication implementation, so do
not reuse one credential across entries that require incompatible tenant
endpoints.

## Change an existing destination

Changing **Configure > Team/Channel** keeps the same config entry and notify
entity. This is useful when a channel is renamed or replaced.

Be careful: all automations using that entity immediately start sending to the
new destination after the entry reloads.

## Naming recommendations

Use names that identify purpose rather than exposing sensitive tenant data:

- `Teams - Operations alerts`
- `Teams - Home notifications`
- `Teams - Test channel`

Avoid embedding tenant IDs, Team IDs, Channel IDs, personal email addresses, or
access roles in entity names.
