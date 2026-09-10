"""Placeholder: Microsoft Graph "teamwork activity feed" notifications.

Not implemented yet — deferred to keep the initial integration scope small.
Requires an Azure AD app-only "Teamwork.Migrate.All" / activity feed
permission and a registered notification topic, which is a larger scope
than the current channel-message notify entity needs. See "Deferred
Features" in ``.github/copilot-instructions.md``.

When implemented, this module should expose something like
``async_send_activity_notification(user_id, activity_type, preview_text,
topic)`` posting to ``/users/{id}/teamwork/sendActivityNotification``,
mixed into ``TeamsGraphApiClient`` the same way ``discovery.py`` and
``messages.py`` are.
"""

from __future__ import annotations
