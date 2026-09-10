"""Placeholder: Bot Framework transport (interactive Adaptive Card actions).

Not implemented yet. Deferred from ``voorstel.md`` — this transport would
let users interact with Adaptive Card buttons (e.g. "Acknowledge alarm",
"Snooze") sent by this integration, which requires registering a Bot
Framework bot (separate Azure resource from the Graph app registration),
handling inbound webhook callbacks, and validating request signatures.

See ``C:\\temp\\skill-ha-teams.md`` for the full rationale on why this was
postponed (adds an inbound webhook surface + a second Azure resource type,
out of scope for a notify-only integration).
"""

from __future__ import annotations
