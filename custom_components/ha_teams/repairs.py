"""Placeholder: Home Assistant repair issues for this integration.

Not implemented yet. Candidate repair issues once needed:

* Missing admin consent for the "Team.ReadBasic.All"/"Channel.ReadBasic.All"
  Graph scopes (currently just falls back to the manual Team/Channel ID
  entry step in the options flow — a repair issue could point the user at
  the exact Entra ID admin consent URL instead).
* Refresh token revoked but reauth not yet completed (currently handled via
  ``ConfigEntryAuthFailed`` → HA's built-in reauth flow, which already
  surfaces a repair-like notification, so a custom repair issue is not
  required unless we want richer guidance text).
"""

from __future__ import annotations
