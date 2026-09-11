# Plan: create a comprehensive GitHub Wiki

## Goal

Create a user-focused GitHub Wiki for `ha-teams` that guides users from
prerequisites through installation, Microsoft Entra configuration, Home
Assistant setup, daily use, troubleshooting, upgrades, and security reporting.

## Wiki structure

- `Home` - overview, supported functionality, quick-start path, and navigation
- `Prerequisites-and-supported-environments` - required Home Assistant,
  Microsoft 365, Teams, Entra, and HACS access
- `Microsoft-Entra-app-registration` - public-client registration, redirect URI,
  delegated Graph permissions, account types, tenant selection, and consent
- `Installation` - HACS and manual installation, restart, upgrades, beta
  releases, and removal
- `Home-Assistant-configuration` - Application Credentials, integration setup,
  OAuth login, Team/Channel selection, manual IDs, options, and reauthentication
- `Sending-notifications` - notify entity discovery, Developer Tools test, and
  practical automation examples
- `Adaptive-Cards` - `ha_teams.send_card`, config entry IDs, card schema,
  examples, limitations, and safe payload guidance
- `Multiple-destinations` - one destination per config entry and managing
  multiple Teams channels/accounts
- `Troubleshooting` - symptom-based guidance for OAuth, consent, tenant,
  discovery, delivery, permissions, reauth, logging, and diagnostics
- `Updating-and-beta-testing` - stable releases, HACS updates, beta releases,
  manual dev installs, rollback, and version checks
- `Security-and-privacy` - token model, stored data, diagnostics redaction,
  least-privilege scopes, safe sharing, and private vulnerability reporting
- `FAQ` - common questions, current limitations, and unsupported/deferred
  features
- `_Sidebar` - persistent navigation for every wiki page
- `_Footer` - links to the repository, releases, issues, and security reporting

## Content principles

- Document only currently implemented behavior as available.
- Clearly label Bot Framework transport, interactive card actions, and activity
  feed notifications as planned and unavailable.
- Use placeholders in all tenant, Team, Channel, entity, and config entry
  examples.
- Explain both My Home Assistant and direct callback redirect URIs.
- Keep command and YAML examples copyable and aligned with current Home
  Assistant syntax.
- Link related wiki pages to provide both a quick-start route and deeper
  reference material.

## Repository and GitHub workflow

1. Create a detailed GitHub issue for the documentation work.
2. Create a `chore/*` branch from `dev`.
3. Add a concise repository change linking the README to the Wiki.
4. Create and populate the separate `<repository>.wiki.git` repository.
5. Open a pull request to `dev` for the repository-side link and plan.
6. Wait for CI and the submitted Copilot review, address all feedback, and
   merge to `dev`.
7. Verify the development pre-release workflow.
8. Do not promote the repository-side documentation change to `main` unless
   explicitly requested.

## Validation

- Verify all internal wiki links resolve.
- Verify the Wiki is enabled and every planned page is visible on GitHub.
- Compare scopes, redirect URIs, service names, fields, and examples with the
  current integration implementation.
- Confirm no secrets, personal data, tenant-private values, or real Teams
  identifiers appear in the pages.
- Confirm README and Wiki navigation point to the published pages.
