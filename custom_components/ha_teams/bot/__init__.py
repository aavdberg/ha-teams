"""Placeholder: Bot Framework transport (interactive Adaptive Card actions).

Not implemented yet. This transport would let users interact with Adaptive
Card buttons (e.g. "Acknowledge alarm", "Snooze") sent by this integration,
which requires registering a Bot Framework bot (separate Azure resource from
the Graph app registration), handling inbound webhook callbacks, and
validating request signatures.

Deferred for now to keep the initial integration scope small — see
"Deferred Features" in ``.github/copilot-instructions.md`` (adds an inbound
webhook surface + a second Azure resource type, out of scope for a
notify-only integration).
"""

from __future__ import annotations
