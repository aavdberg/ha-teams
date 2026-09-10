"""Placeholder: Bot Framework inbound request validation.

Not implemented yet. Would verify the JWT bearer token Microsoft attaches
to inbound bot callbacks (issuer, audience = bot's app ID, signature via
Microsoft's OpenID metadata/JWKS), and should also enforce an allowlist for
which card actions are accepted and replay-protection (see ``voorstel.md``
teststrategie: "allowlist voor kaartacties", "replaypreventie").
"""

from __future__ import annotations
