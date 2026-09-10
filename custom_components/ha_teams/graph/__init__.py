"""Microsoft Graph API client package.

Combines the low-level HTTP transport (``client.py``) with the discovery
(``discovery.py``) and messaging (``messages.py``) endpoint mixins into the
single :class:`TeamsGraphApiClient` used by the rest of the integration.

Planned future transports (see "Deferred Features" in
``.github/copilot-instructions.md``) live alongside these as their own
modules so they can be wired in without reshaping this package again:

* ``activity.py`` — Graph "teamwork activity feed" notifications.
* ``app_installation.py`` — installing/uninstalling the HA bot/app for a
  team, a prerequisite for the Bot Framework transport in ``bot/``.
"""

from __future__ import annotations

from .client import GraphApiError, GraphAuthError, GraphHttpClient
from .discovery import GraphDiscoveryMixin
from .messages import GraphMessagesMixin


class TeamsGraphApiClient(GraphDiscoveryMixin, GraphMessagesMixin, GraphHttpClient):
    """Full Microsoft Graph API client used by this integration.

    Composed from mixins so each concern (transport, discovery, messaging)
    can be tested and extended independently.
    """


__all__ = ["GraphApiError", "GraphAuthError", "TeamsGraphApiClient"]
