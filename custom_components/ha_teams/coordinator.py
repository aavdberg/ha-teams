"""Placeholder: DataUpdateCoordinator for periodic Team/Channel refresh.

Not implemented yet. The current integration is notify-only and doesn't
need polling: the destination channel is fixed at config/options-flow time
and messages are sent on demand. A coordinator would become useful if this
integration grows read-side features (e.g. periodically refreshing the
list of joined Teams/Channels to detect renames, or polling for incoming
mentions once the Bot Framework transport in ``bot/`` exists).
"""

from __future__ import annotations
