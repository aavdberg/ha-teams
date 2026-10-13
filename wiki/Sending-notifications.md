# Sending notifications

ha-teams creates one notify entity for each configured integration entry. The
entity sends to the Team and Channel currently selected in that entry's
options.

## Find the notify entity

Go to:

**Settings > Devices & services > Microsoft Teams > Entities**

Copy the exact entity ID. Examples use:

```text
notify.your_microsoft_teams_entity
```

Replace it with your actual entity ID.

## Send a test from Developer Tools

1. Open **Developer Tools > Actions**.
2. Select `notify.send_message`.
3. Choose the Microsoft Teams notify entity as the target.
4. Enter a message and optional title.
5. Run the action.

Equivalent YAML:

```yaml
action: notify.send_message
target:
  entity_id: notify.your_microsoft_teams_entity
data:
  title: "Home Assistant test"
  message: "The Microsoft Teams integration is working."
```

If the entity is unavailable, configure the destination under the integration's
**Configure** action.

## Basic automation

```yaml
alias: Notify Teams when motion is detected
description: Send a Teams message when front door motion starts.
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

## Include an entity state

```yaml
alias: Notify Teams about a low battery
description: Send a warning when a battery sensor drops below 20 percent.
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
        is at {{ states('sensor.device_battery') }}%.
mode: single
```

## Multi-line status message

```yaml
alias: Send nightly status to Teams
description: Summarize selected Home Assistant states.
triggers:
  - trigger: time
    at: "22:00:00"
actions:
  - action: notify.send_message
    target:
      entity_id: notify.your_microsoft_teams_entity
    data:
      title: "Nightly status"
      message: |
        Alarm: {{ states('alarm_control_panel.home_alarm') }}
        Front door: {{ states('binary_sensor.front_door') }}
        Temperature: {{ states('sensor.living_room_temperature') }} °C
mode: single
```

## Use variables safely

Home Assistant renders the title and message before ha-teams submits the text to
Microsoft Graph. Use defaults for missing or unavailable values:

```yaml
message: >-
  Temperature is
  {{ states('sensor.living_room_temperature') | default('unknown', true) }} °C.
```

Avoid including secrets, access tokens, alarm codes, private URLs, or
unnecessary personal data in Teams messages.

## Message behavior

- The title and message are combined into a Microsoft Graph channel message.
- Messages appear as the signed-in Microsoft user.
- Microsoft Teams controls final Markdown rendering and link previews.
- Transient HTTP 429 and server errors are retried automatically.
- Authentication failures trigger Home Assistant reauthentication.
- Other Graph errors are logged and the action fails rather than pretending
  the message was delivered.

For rich layouts, see [Adaptive Cards](Adaptive-Cards). For separate
destinations, see [Multiple destinations](Multiple-destinations).
