# Plan: add a repository security policy

## Goal
Add a `SECURITY.md` file at the repository root so security reports and vulnerability disclosure are handled clearly and consistently for the `ha-teams` project.

## Proposed change
- Create a root-level `SECURITY.md` file.
- Document which releases and branches receive security fixes.
- Enable and document GitHub Private Vulnerability Reporting as the disclosure route.
- Define integration-specific security scope for OAuth/PKCE, Microsoft Graph,
  diagnostics, logging, permissions, and message payload handling.
- Explain which reports belong upstream with Home Assistant, Microsoft, or a
  dependency maintainer.
- Define safe-testing, sensitive-data redaction, coordinated-disclosure, and
  response expectations.

## Files involved
- `SECURITY.md` (new)

## Validation
- Confirm GitHub Private Vulnerability Reporting is enabled.
- Confirm the file renders correctly and follows repository conventions.
- Confirm no existing security disclosure file conflicts with the new policy.
- Confirm no private contact details or sensitive repository data are included.
