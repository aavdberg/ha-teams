# Adaptive Cards

Use the `ha_teams.send_card` action to send a full Adaptive Card to the Team and
Channel configured on a ha-teams entry.

## Requirements

- A configured ha-teams config entry.
- Microsoft Graph delegated transport.
- A valid Adaptive Card object.
- The signed-in user must be allowed to send to the configured channel.

## Use the visual action editor

The easiest way to obtain the config entry ID safely is:

1. Open **Developer Tools > Actions** or an automation action editor.
2. Select **Microsoft Teams: Send Adaptive Card**.
3. Select the desired config entry from the **Config entry** selector.
4. Enter the card object.

The visual editor stores the selected config entry ID in the generated YAML.

## Minimal example

```yaml
action: ha_teams.send_card
data:
  config_entry_id: 0123456789abcdef0123456789abcdef
  card:
    type: AdaptiveCard
    version: "1.5"
    body:
      - type: TextBlock
        text: Home Assistant
        weight: Bolder
        size: Medium
      - type: TextBlock
        text: The pump is active.
        wrap: true
```

Replace the example config entry ID by selecting your entry in the Home
Assistant UI.

## Automation example with templates

```yaml
alias: Send temperature card to Teams
description: Send a formatted temperature card every morning.
triggers:
  - trigger: time
    at: "08:00:00"
actions:
  - action: ha_teams.send_card
    data:
      config_entry_id: 0123456789abcdef0123456789abcdef
      card:
        type: AdaptiveCard
        version: "1.5"
        body:
          - type: TextBlock
            text: Morning climate report
            weight: Bolder
            size: Large
          - type: FactSet
            facts:
              - title: Living room
                value: >-
                  {{ states('sensor.living_room_temperature') }} °C
              - title: Humidity
                value: >-
                  {{ states('sensor.living_room_humidity') }}%
          - type: TextBlock
            text: "Generated at {{ now().strftime('%Y-%m-%d %H:%M') }}"
            isSubtle: true
            wrap: true
mode: single
```

Home Assistant templates in action data are rendered before the card is passed
to ha-teams.

## Open a URL

Client-side actions such as opening a safe HTTPS URL can be included:

```yaml
card:
  type: AdaptiveCard
  version: "1.5"
  body:
    - type: TextBlock
      text: Review the Home Assistant dashboard
      wrap: true
  actions:
    - type: Action.OpenUrl
      title: Open dashboard
      url: https://homeassistant.example.com/
```

Do not include signed URLs, embedded credentials, access tokens, or internal
URLs that should not be shared with everyone who can read the channel.

## Validation and schema behavior

ha-teams expects `card` to be an object and wraps it in the Microsoft Graph
chat message attachment format. Microsoft Teams validates and renders the
Adaptive Card.

Recommended practices:

- Set `type` to `AdaptiveCard`.
- Set `version` explicitly to `"1.5"` for predictable behavior.
- If `version` is omitted, ha-teams adds its supported default version, which
  is currently `"1.5"`.
- Set `wrap: true` on variable-length text.
- Test cards in the target Teams clients used by your users.
- Keep payloads reasonably small.
- Use only Adaptive Card elements supported by Microsoft Teams.

The integration does not currently perform complete Adaptive Card schema
validation. A malformed or unsupported card can be rejected by Microsoft Graph
or rendered differently by Teams clients.

## Interactive-action limitation

`Action.Submit`, `Action.Execute`, acknowledge buttons, snooze buttons, and
other actions that require a callback to Home Assistant are not supported.
Those features require the planned Bot Framework transport and a secure inbound
callback endpoint.

Use `Action.OpenUrl` only for actions that can be completed entirely by opening
a URL.

## Common errors

| Symptom | Likely cause |
| --- | --- |
| Unknown config entry | The ID is incorrect or belongs to another integration |
| Destination is not configured | Select a Team and Channel in entry options |
| Unsupported transport | The selected entry is not using Graph delegated transport |
| HTTP 400 | Invalid or unsupported card payload |
| HTTP 401/403 | Authentication, consent, membership, or Graph permission problem |

See [Troubleshooting](Troubleshooting) for detailed steps.
