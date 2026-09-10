"""Placeholder: Microsoft Graph "teamwork activity feed" notifications.

Not implemented yet. Deferred from ``voorstel.md`` (Activity Feed
Transport) — see ``C:\\temp\\skill-ha-teams.md`` for the rationale on why
this was postponed (requires an Azure AD app-only "Teamwork.Migrate.All" /
activity feed permission and a registered notification topic, which is a
larger scope than the current channel-message notify entity needs).

When implemented, this module should expose something like
``async_send_activity_notification(user_id, activity_type, preview_text,
topic)`` posting to ``/users/{id}/teamwork/sendActivityNotification``,
mixed into ``TeamsGraphApiClient`` the same way ``discovery.py`` and
``messages.py`` are.
"""

from __future__ import annotations
