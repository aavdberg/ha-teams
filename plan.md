# Plan: organize the ha-teams roadmap in GitHub Projects

## Goal

Turn the deferred roadmap into actionable GitHub issues and public GitHub
Projects so planned work can be prioritized, implemented, and reviewed without
losing architectural dependencies.

## Projects

### Bot Framework and Interactive Cards

Track the future `teams_bot` transport, including Bot Framework authentication,
Teams app packaging and installation, conversation references, secure inbound
callbacks, proactive messages, and interactive Adaptive Card actions.

### Teams Activity Feed Notifications

Track Graph activity notifications, permission and consent design, application
installation, activity payload rendering, user targeting, Home Assistant
actions, and end-to-end testing.

### Scalable Configuration and Notification Delivery

Track config subentries or an equivalent multi-destination model, per-entry
tenant/cloud selection, durable notification queues, and digest/batching
support.

### Reliability, Repairs, and Integration Testing

Track destination health detection, repair issues, optional read-side
coordination, improved diagnostics/observability, and a real Home Assistant
integration test harness.

## Project configuration

Each project will:

- Be public and linked to `aavdberg/ha-teams`.
- Include a detailed description and README explaining scope, dependencies,
  completion criteria, and exclusions.
- Use `Status`, `Priority`, and `Roadmap phase` fields.
- Provide consistent backlog, delivery board, high-priority, and
  architecture/foundation views.
- Contain detailed English GitHub issues rather than vague draft notes.
- Mark prerequisite/architecture work as higher priority than dependent UI or
  documentation work.

## Issue principles

- Create one issue per independently reviewable deliverable.
- Document context, rationale, implementation scope, security/privacy concerns,
  dependencies, acceptance criteria, and verification.
- Reuse the existing placeholder modules instead of restructuring the package.
- Keep currently unsupported features clearly separated from released behavior.
- Avoid assigning dates until capacity and implementation order are agreed.

## Validation

- Confirm all four projects are visible and linked to the repository.
- Confirm every roadmap issue is assigned to exactly one primary project.
- Confirm project fields and issue metadata are populated consistently.
- Confirm every project exposes direct links to its backlog, delivery board,
  high-priority, and architecture/foundation views.
- Confirm the external GitHub Project READMEs for Projects 3-6 contain those
  links; Project README metadata is configured on GitHub and is not stored in
  this repository's git diff.
- Confirm the repository Issues sidebar lists the six shared Issue Views.
- Confirm dependencies are described in issue bodies.
- Confirm no existing issue is duplicated.
