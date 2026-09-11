# Updating and beta testing

## Stable updates through HACS

1. Open HACS.
2. Open **Microsoft Teams**.
3. Review the release notes.
4. Download the offered stable update.
5. Restart Home Assistant.
6. Confirm the integration entry loads and send a test message.

Back up Home Assistant before updates according to your normal operational
practice.

## Manual stable updates

1. Download the desired release archive.
2. Stop or safely prepare Home Assistant for the file replacement.
3. Replace the complete `/config/custom_components/ha_teams` directory.
4. Restart Home Assistant.
5. Confirm the version and send a test message.

Do not overlay only selected files; removed or renamed files from an older
version can cause unpredictable behavior.

## Check the installed version

Depending on Home Assistant and HACS versions, the installed version is visible
in HACS or the integration information.

For a manual check, open:

```text
/config/custom_components/ha_teams/manifest.json
```

Read the `version` field. Do not edit it to simulate an upgrade.

## Test beta releases through HACS

Merges to the `dev` branch publish pre-releases such as:

```text
v0.4.0-beta.8
```

In HACS:

1. Enable **Show beta releases** in HACS experimental settings.
2. Open the Microsoft Teams repository.
3. Select the desired beta version.
4. Download it and restart Home Assistant.
5. Test authentication, destination selection, plain notifications, and any
   changed features.

Beta releases can contain incomplete or recently changed behavior. Use them in
an environment where rollback is practical.

## Test the current dev branch manually

Download:

```text
https://github.com/aavdberg/ha-teams/archive/refs/heads/dev.zip
```

Extract and copy only `custom_components/ha_teams` to the Home Assistant custom
components directory, then restart.

The moving `dev` branch is less reproducible than a tagged beta. Prefer beta
tags for ongoing testing.

## Roll back

1. Record the current version and create a Home Assistant backup.
2. In HACS, select the previously working release, or manually install its full
   integration directory.
3. Restart Home Assistant.
4. Confirm the config entry loads and send a test notification.

Configuration migrations are not currently expected, but restoring a full Home
Assistant backup is the safest rollback when a future release changes stored
data.

## Report beta problems

Open a public issue for normal regressions and include:

- Exact beta tag
- Home Assistant version
- Upgrade source version
- Reproduction steps
- Redacted logs
- Whether the issue also occurs on the latest stable release

Never publish tokens, tenant-private identifiers, Team/Channel IDs, or private
message content.

## Release channels

| Channel | Source | Intended audience |
| --- | --- | --- |
| Stable | `main` and normal GitHub releases | Regular users |
| Beta | Tagged pre-releases generated from `dev` | Testers who can diagnose and roll back |
| Development | Moving `dev` branch | Short-lived development testing |
