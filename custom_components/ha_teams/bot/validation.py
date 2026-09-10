"""Placeholder: Bot Framework inbound request validation.

Not implemented yet. Would verify the JWT bearer token Microsoft attaches
to inbound bot callbacks (issuer, audience = bot's app ID, signature via
Microsoft's OpenID metadata/JWKS), and should also enforce an allowlist for
which card actions are accepted, plus replay protection (reject/dedupe
requests with an already-seen activity ID or an expired timestamp).
"""

from __future__ import annotations
