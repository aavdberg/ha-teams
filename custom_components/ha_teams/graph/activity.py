"""Placeholder: Microsoft Graph "teamwork activity feed" notifications.

Not implemented yet — deferred to keep the initial integration scope small.
Requires the ``TeamsActivity.Send`` Graph permission (delegated) — or
``TeamsActivity.Send.User``/``TeamsActivity.Send.Group`` via
resource-specific consent for application permissions — plus a registered
notification topic, which is a larger scope than the current
channel-message notify entity needs. See "Deferred Features" in
``.github/copilot-instructions.md``.

When implemented, this module should expose something like
``async_send_activity_notification(user_id, activity_type, preview_text,
topic)`` posting to ``/users/{id}/teamwork/sendActivityNotification``,
mixed into ``TeamsGraphApiClient`` the same way ``discovery.py`` and
``messages.py`` are.
"""

from __future__ import annotations
