# Security Policy

Thank you for helping keep `ha-teams` and its users safe. We take security
reports seriously and appreciate responsible disclosure.

## Supported versions

Security fixes are developed against the current maintained code and released
as part of a new `ha-teams` version.

| Version | Supported |
| --- | --- |
| Latest stable release | Yes |
| Current `dev` branch | Yes, for development and upcoming releases |
| Older releases | No |

Reports affecting an older release are still useful when the vulnerability also
exists in the current maintained version. Users may need to upgrade to receive a
security fix.

## How to report a vulnerability

**Do not open a public GitHub issue, discussion, or pull request for a suspected
security vulnerability.**

Use
[GitHub Private Vulnerability Reporting](https://github.com/aavdberg/ha-teams/security/advisories/new)
to submit the report confidentially. This allows the reporter and maintainer to
discuss the issue and coordinate a fix without exposing users before a patched
release is available.

If you are unsure whether an issue is security-sensitive, report it privately
first. It can be moved to the public issue tracker later if appropriate.

## What to include

Provide enough detail to reproduce and assess the issue:

- A clear description of the vulnerability and its security impact
- The affected `ha-teams` and Home Assistant versions
- Required attacker access or preconditions
- Reproduction steps or a minimal proof of concept
- Expected and actual behavior
- Suggested mitigations or fixes, if known
- Redacted logs, diagnostics, or configuration details when relevant

## Response expectations

The maintainer will make a best effort to:

- Acknowledge the report and determine whether it is in scope
- Keep the reporter informed when the status materially changes
- Develop and validate a fix according to the severity and complexity
- Coordinate publication of an advisory and patched release when appropriate

Please allow time for investigation and remediation before public disclosure.
Do not publish exploit details, proof-of-concept code, or identifying tenant data
until disclosure has been coordinated.

## Scope

`ha-teams` is a Home Assistant custom integration that authenticates through the
Microsoft identity platform and sends Microsoft Teams channel messages through
the Microsoft Graph API.

Security issues in scope include:

- OAuth 2.0, PKCE, authorization-state, or token-handling flaws
- Authentication or authorization bypasses
- Requests for unnecessary Microsoft Graph permissions
- Cross-tenant or cross-config-entry data exposure
- Exposure of tokens, authorization codes, tenant data, Teams identifiers, or
  message content through storage, diagnostics, logs, or errors
- Unsafe rendering or construction of Microsoft Graph message and Adaptive Card
  payloads
- Unintended requests to attacker-controlled endpoints
- Dependency vulnerabilities that are exploitable through this integration

The following normally belong in a public bug report rather than a private
security report:

- Setup, configuration, or compatibility problems without a security impact
- Microsoft Graph permission or consent errors caused by an incorrectly
  configured app registration
- Notification formatting or delivery failures that do not expose data or cross
  a security boundary
- Feature requests and hardening suggestions without a concrete vulnerability

Vulnerabilities in Home Assistant, Microsoft Graph, the Microsoft identity
platform, or a third-party dependency that do not arise from `ha-teams` should
be reported to the relevant upstream project or vendor. If `ha-teams` makes an
upstream vulnerability exploitable, report that integration-specific impact
privately here as well.

## Safe testing and sensitive data

Only test with systems, tenants, accounts, teams, and channels that you own or
are explicitly authorized to use. Do not:

- Access, modify, or delete another person's data
- Disrupt Home Assistant, Microsoft 365, or Teams services
- Perform denial-of-service or high-volume automated testing
- Use social engineering, phishing, or physical attacks
- Retain more data than is necessary to demonstrate the issue

Never include real secrets or private tenant data in a report. Redact:

- Access tokens, refresh tokens, authorization codes, and Home Assistant tokens
- Client secrets or other credentials
- Tenant, team, channel, user, and message identifiers
- Private message content, names, email addresses, and diagnostic data

Use clearly artificial placeholders in screenshots, logs, payloads, and proofs
of concept. If a sensitive value is essential to understanding the report,
describe its type and behavior instead of sharing the value itself.

## Security updates

Confirmed vulnerabilities may be handled through a private GitHub security
advisory. Depending on impact, the resolution may include a patched release,
upgrade guidance, mitigations, and public credit for the reporter if requested
and appropriate.
