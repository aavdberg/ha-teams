# Installation

HACS is the recommended installation method because it provides update
notifications and straightforward upgrades.

## Install with HACS

Use the repository button:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=aavdberg&repository=ha-teams&category=integration)

Or add it manually:

1. Open **HACS** in Home Assistant.
2. Open the three-dot menu and select **Custom repositories**.
3. Enter:

   ```text
   https://github.com/aavdberg/ha-teams
   ```

4. Select category **Integration**.
5. Find **Microsoft Teams** and select **Download**.
6. Restart Home Assistant.

The integration must be installed and Home Assistant restarted before
**Microsoft Teams** appears in Application Credentials or Add Integration.

## Manual installation

1. Download the latest stable source from the
   [releases page](https://github.com/aavdberg/ha-teams/releases).
2. Extract the archive.
3. Copy the entire `custom_components/ha_teams` directory to:

   ```text
   /config/custom_components/ha_teams
   ```

4. Confirm the final path contains `manifest.json`, `config_flow.py`, and the
   other integration files directly. Avoid an extra nested `ha_teams` folder.
5. Restart Home Assistant.

## Confirm installation

After restart:

1. Go to **Settings > Devices & services**.
2. Select **Add integration**.
3. Search for **Microsoft Teams**.

If it is missing:

- Confirm the directory name is exactly `ha_teams`.
- Confirm Home Assistant was restarted, not only reloaded.
- Check **Settings > System > Logs** for manifest or import errors.
- Confirm Home Assistant meets the minimum supported version.
- Clear the browser cache only after confirming the server-side installation.

## Updating

For HACS installs, open the integration in HACS and install the offered stable
update, then restart Home Assistant.

For manual installs, replace the complete integration directory with the files
from the desired release and restart. Do not mix files from different
versions.

See [Updating and beta testing](Updating-and-beta-testing) for pre-releases,
rollback, and version checks.

## Removing the integration

1. Remove every Microsoft Teams config entry from
   **Settings > Devices & services**.
2. Restart Home Assistant if requested.
3. Remove the integration through HACS, or delete only:

   ```text
   /config/custom_components/ha_teams
   ```

4. Restart Home Assistant.
5. Optionally remove the related Home Assistant Application Credential.
6. Optionally revoke user consent or remove the app registration in Microsoft
   Entra if it is no longer used.

Removing the files before removing config entries can leave unavailable
entries in Home Assistant until the integration is reinstalled or the entries
are removed.
