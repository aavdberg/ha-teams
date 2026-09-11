# Roadmap

The ha-teams roadmap is organized into four public GitHub Projects and matching
repository milestones. Projects show day-to-day status, priority, and delivery
phase; milestones group the issues that together deliver a releasable
capability.

No target dates are assigned yet. Work should follow the documented
dependencies and should not be presented as available until it is implemented,
tested, documented, reviewed, and released.

## Projects and milestones

| Workstream | Project | Milestone | Scope |
| --- | --- | --- | --- |
| Bot Framework and Interactive Cards | [Project 3](https://github.com/users/aavdberg/projects/3) | [Milestone 1](https://github.com/aavdberg/ha-teams/milestone/1) | Bot/app sender, proactive activities, conversation references, secure callbacks, and interactive cards |
| Teams Activity Feed Notifications | [Project 4](https://github.com/users/aavdberg/projects/4) | [Milestone 2](https://github.com/aavdberg/ha-teams/milestone/2) | Activity types, permissions, app installation, Graph payloads, recipient targeting, tests, and documentation |
| Scalable Configuration and Notification Delivery | [Project 5](https://github.com/users/aavdberg/projects/5) | [Milestone 3](https://github.com/aavdberg/ha-teams/milestone/3) | Config subentries for scalable destination management, cloud profiles, optional durable queues, and digest notifications |
| Reliability, Repairs, and Integration Testing | [Project 6](https://github.com/users/aavdberg/projects/6) | [Milestone 4](https://github.com/aavdberg/ha-teams/milestone/4) | Home Assistant lifecycle tests, repairs, destination health, diagnostics, and safe logging |

## Project views

Every project provides the same views:

- **Roadmap backlog**: complete table with status, priority, phase, assignees,
  milestone, and labels.
- **Delivery board**: board layout for moving work through project status.
- **High priority**: filtered to P0 and P1 work.
- **Architecture and foundations**: filtered to Discovery and Foundation work
  that should generally precede dependent implementation.

GitHub can collapse the view tabs depending on browser width or UI state. Use
these direct links if the tabs are not visible:

| Project | Backlog | Delivery board | High priority | Architecture and foundations |
| --- | --- | --- | --- | --- |
| Bot Framework and Interactive Cards | [Open](https://github.com/users/aavdberg/projects/3/views/1) | [Open](https://github.com/users/aavdberg/projects/3/views/2) | [Open](https://github.com/users/aavdberg/projects/3/views/3) | [Open](https://github.com/users/aavdberg/projects/3/views/4) |
| Teams Activity Feed Notifications | [Open](https://github.com/users/aavdberg/projects/4/views/1) | [Open](https://github.com/users/aavdberg/projects/4/views/2) | [Open](https://github.com/users/aavdberg/projects/4/views/3) | [Open](https://github.com/users/aavdberg/projects/4/views/4) |
| Scalable Configuration and Notification Delivery | [Open](https://github.com/users/aavdberg/projects/5/views/1) | [Open](https://github.com/users/aavdberg/projects/5/views/2) | [Open](https://github.com/users/aavdberg/projects/5/views/3) | [Open](https://github.com/users/aavdberg/projects/5/views/4) |
| Reliability, Repairs, and Integration Testing | [Open](https://github.com/users/aavdberg/projects/6/views/1) | [Open](https://github.com/users/aavdberg/projects/6/views/2) | [Open](https://github.com/users/aavdberg/projects/6/views/3) | [Open](https://github.com/users/aavdberg/projects/6/views/4) |

The same four direct links are stored in each GitHub Project's README. Project
README content is GitHub project metadata, so it does not appear as a file in
the repository pull request.

## Repository Issue Views

The repository also provides shared
[Issue Views](https://github.com/aavdberg/ha-teams/issues/views). These are
separate from the views inside each GitHub Project and provide cross-project
filters from the repository Issues sidebar:

- **Open roadmap**
- **Bot Framework**
- **Activity Feed**
- **Scalable configuration**
- **Reliability and testing**
- **Security-sensitive roadmap**

## Recommended implementation order

1. Build the real Home Assistant integration test harness in
   [#61](https://github.com/aavdberg/ha-teams/issues/61) and lifecycle coverage
   in [#62](https://github.com/aavdberg/ha-teams/issues/62).
2. Complete architecture and permission decisions before implementing new
   transports or configuration models:
   [#45](https://github.com/aavdberg/ha-teams/issues/45),
   [#51](https://github.com/aavdberg/ha-teams/issues/51), and
   [#56](https://github.com/aavdberg/ha-teams/issues/56).
3. Implement security-sensitive foundations before exposing user-facing bot or
   Activity Feed actions.
4. Add migration, diagnostics, end-to-end tests, documentation, and release
   validation before marking a milestone complete.

## Bot Framework and Interactive Cards

- [#45 Design the transport architecture and threat model](https://github.com/aavdberg/ha-teams/issues/45)
- [#46 Create the Teams app package and installation lifecycle](https://github.com/aavdberg/ha-teams/issues/46)
- [#47 Implement Bot Connector authentication and proactive sending](https://github.com/aavdberg/ha-teams/issues/47)
- [#48 Capture and manage conversation references](https://github.com/aavdberg/ha-teams/issues/48)
- [#49 Validate callbacks and prevent replay](https://github.com/aavdberg/ha-teams/issues/49)
- [#50 Expose the bot transport and safe interactive actions](https://github.com/aavdberg/ha-teams/issues/50)

## Teams Activity Feed Notifications

- [#51 Define permissions, topics, and consent](https://github.com/aavdberg/ha-teams/issues/51)
- [#52 Implement Teams app installation checks](https://github.com/aavdberg/ha-teams/issues/52)
- [#53 Implement the Graph client and renderer](https://github.com/aavdberg/ha-teams/issues/53)
- [#54 Add Home Assistant actions and recipient configuration](https://github.com/aavdberg/ha-teams/issues/54)
- [#55 Complete lifecycle tests, diagnostics, and documentation](https://github.com/aavdberg/ha-teams/issues/55)

## Scalable Configuration and Notification Delivery

- [#56 Design config subentries and migration](https://github.com/aavdberg/ha-teams/issues/56)
- [#57 Implement multiple destinations and entities](https://github.com/aavdberg/ha-teams/issues/57)
- [#58 Support explicit tenant and cloud endpoint profiles](https://github.com/aavdberg/ha-teams/issues/58)
- [#59 Add an optional durable notification queue](https://github.com/aavdberg/ha-teams/issues/59)
- [#60 Implement digest and event batching](https://github.com/aavdberg/ha-teams/issues/60)

## Reliability, Repairs, and Integration Testing

- [#61 Adopt a Home Assistant integration test harness](https://github.com/aavdberg/ha-teams/issues/61)
- [#62 Cover current integration lifecycles end to end](https://github.com/aavdberg/ha-teams/issues/62)
- [#63 Add repair issues for consent and destinations](https://github.com/aavdberg/ha-teams/issues/63)
- [#64 Evaluate minimal destination health polling](https://github.com/aavdberg/ha-teams/issues/64)
- [#65 Harden diagnostics and logging](https://github.com/aavdberg/ha-teams/issues/65)

## Current availability

The roadmap does not change the current supported feature set. Today:

- Microsoft Graph delegated channel messaging is supported.
- Plain notifications and Adaptive Cards are supported.
- Messages are sent as the signed-in user.
- Bot transport, interactive callbacks, Activity Feed notifications,
  destination config subentries, queues, and digests are not implemented.

Follow the projects or individual issues for status updates.
