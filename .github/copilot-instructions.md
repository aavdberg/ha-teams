# GitHub Copilot Instructions — ha-teams

This file provides persistent context for GitHub Copilot so it understands the project
without needing to re-learn the codebase on every session.

---

## Project Overview

**ha-teams** is a Home Assistant custom integration that sends notifications to a
Microsoft Teams channel via the **Microsoft Graph API**, authenticated with the
**OAuth 2.0 Authorization Code flow + PKCE** (RFC 7636). It replaces the legacy
Incoming Webhook / Office 365 Connector approach that Microsoft has retired.

- **Repo**: https://github.com/aavdberg/ha-teams
- **Domain**: `ha_teams`
- **HA minimum version**: 2024.6
- **Python target**: 3.12
- **Linter**: ruff (configured in `pyproject.toml`)

---

## Repository Structure

```
custom_components/ha_teams/
├── __init__.py                # Entry setup/unload, entry.runtime_data, ha_teams.send_card service
├── manifest.json               # Integration metadata, version
├── const.py                    # Domain, OAuth endpoints/scopes, retry tuning, service/attr names
├── pkce_oauth2.py               # PKCE-enabled OAuth2 implementation (code_verifier/code_challenge)
├── application_credentials.py  # Authorize/token endpoints for the OAuth2 + PKCE flow
├── api.py                       # Microsoft Graph API client (retry/backoff, Adaptive Cards)
├── config_flow.py               # OAuth2 (PKCE) login flow + reauth + team/channel options flow
├── notify.py                    # NotifyEntity that posts channel messages
├── diagnostics.py               # Redacted diagnostics (tokens, team/channel IDs)
├── services.yaml                # ha_teams.send_card service definition
├── strings.json                 # Source-of-truth translation strings (English)
└── translations/
    └── en.json

tests/
├── conftest.py                  # Stubs homeassistant.* modules (no full HA core dependency)
├── test_pkce_oauth2.py          # PKCE code_verifier/code_challenge unit tests
├── test_api.py                  # Retry classification + Adaptive Card payload unit tests
└── test_api_client.py           # TeamsGraphApiClient behaviour with a fake aiohttp session

.github/
├── workflows/
│   ├── lint.yml               # Ruff lint + format check, pytest, HACS validation (push/PR to main & dev)
│   ├── hassfest.yml           # Home Assistant hassfest validation (push/PR/daily/manual)
│   ├── gitleaks.yml           # Secret scanning (push/PR/daily/manual)
│   ├── copilot-review.yml     # Copilot auto code review on PRs to main & dev
│   ├── pre-release.yml        # Auto pre-release tag on every push to dev (for HACS beta testing)
│   └── release.yml            # Auto GitHub Release on merge to main (based on manifest version)
└── copilot-instructions.md    # THIS FILE — update when architecture/auth model changes
```

---

## Authentication Model

- **OAuth 2.0 Authorization Code Flow + PKCE** against Microsoft identity platform
  (`https://login.microsoftonline.com/common/oauth2/v2.0/{authorize,token}`).
- No client secret required — the Entra ID app registration is a "public client"
  ("Allow public client flows" = Yes).
- PKCE `code_verifier`/`code_challenge` (S256) generated per authorization attempt in
  `pkce_oauth2.MicrosoftGraphPkceOAuth2Implementation`.
- Delegated Graph scopes: `openid profile offline_access ChannelMessage.Send
  Team.ReadBasic.All Channel.ReadBasic.All`.
- Team/channel selection happens in the **Options flow** (`config_flow.py`), not the
  initial config flow, so it can reuse the fully-managed `OAuth2Session` tied to the
  real config entry (token refresh/storage already wired up).
- Token refresh failures / revoked consent raise `ConfigEntryAuthFailed`, which starts
  Home Assistant's reauth flow (`async_step_reauth` → `async_step_reauth_confirm`).

## Microsoft Graph API Client (`api.py`)

- Retries HTTP 429 (respecting `Retry-After`) and 5xx with exponential backoff + jitter,
  up to `MAX_RETRY_ATTEMPTS` (4). Never retries 4xx.
- HTTP 401/403 raise `GraphAuthError` immediately (no retry) so callers can trigger reauth
  instead of retrying against a permanently broken token.
- Supports both plain-text channel messages (`async_send_channel_message`) and full
  Adaptive Cards (`async_send_adaptive_card`, exposed as the `ha_teams.send_card` service).

---

## Branching Strategy

| Branch | Purpose |
|---|---|
| `main` | Production — HACS users install from here; auto GitHub Release on merge |
| `dev` | Development & testing — all features merge here first |
| `feature/*` | Individual features — PR to `dev` |
| `fix/*` | Bug fixes — PR to `dev` |
| `chore/*` | Non-code changes (docs, CI, repo tooling) — PR directly to `main` if completely unrelated to integration code |

> **Note:** Changes unrelated to the Home Assistant integration (e.g. CI workflows, docs, repo scripts) should be kept separate from integration changes and can be merged directly into `main` via PR without triggering dev beta pre-releases.

Both `main` and `dev` are protected: PRs required, ruff lint must pass.

### ⚠️ CRITICAL RULE — Mandatory workflow for every change:

Every change — no matter how small — **must** follow these steps in order:

1. **Plan** — Analyse the problem, explore the codebase, and create a clear plan
   (what will change, which files, why). Save the plan to `plan.md`.
2. **Confirm** — Present the plan to the user and **ask for approval** before writing
   any code. Do **not** proceed until the user confirms.
3. **Issue** — Create a GitHub Issue describing the change (bug report, feature request,
   or chore). Reference any related issues/PRs.
4. **Branch** — Create a branch from `dev` following the naming convention:
   ```
   git checkout dev && git pull
   git checkout -b fix/my-fix          # or feature/, chore/
   ```
5. **Implement** — Make the code changes, run linter (`ruff check custom_components/` + `ruff format --check custom_components/`)
   and tests (`python -m pytest tests/ -v`), and commit with Conventional Commits.
6. **Push & PR** — Push the branch and open a Pull Request targeting `dev`:
   ```
   git push -u origin fix/my-fix
   gh pr create --base dev --head fix/my-fix --title "..." --body "..."
   ```
7. **CI** — Wait for all CI checks to pass (ruff lint, ruff format, pytest, HACS
   validation, hassfest, gitleaks, and the "Request Copilot Code Review" workflow).
8. **Review** — After CI passes, **wait for the Copilot code review to actually be
   submitted** before merging. The "Request Copilot Code Review" workflow only
   *triggers* the review; the review comments arrive asynchronously a short time
   later. Verify the review has been submitted by polling:
   ```
   gh pr view <N> --json reviews -q '.reviews[] | select(.author.login=="copilot-pull-request-reviewer") | .submittedAt'
   ```
   (Or use the GitHub API `get_reviews` / `get_review_comments` methods.)
   Only proceed when the review is present. Then:
   - Retrieve and read all review comments using the GitHub API / `gh` CLI.
   - Evaluate each comment/suggestion to decide whether a code fix is needed or not.
   - Add a comment (reply) to each review thread explaining the decision or what fix was implemented.
   - If a code fix is needed, push the commit, wait for CI, and re-check.
   - **Resolve** the review conversation threads (using GraphQL `resolveReviewThread` / `resolve_thread` tool).
   - Repeat until all review conversations are resolved.
9. **Merge** — Once CI passes and all review comments are resolved, merge the PR into `dev`:
   ```
   gh pr merge <PR_NUMBER> --squash --delete-branch
   ```
10. **Verify dev pre-release** — After the merge, confirm that the `Pre-release`
    workflow created a new `v<version>-beta.<N>` tag/release on `dev` (e.g. `v0.2.0-beta.1`):
    ```
    gh run list --workflow pre-release.yml --limit 1
    gh release list --limit 3
    ```
    If the workflow did not run or failed, investigate before moving on. This
    pre-release is what HACS beta-testers install, so missing it silently breaks
    their update path.

**NEVER commit or push directly to `dev` or `main`.**
Even as admin (bypassed protection), direct pushes skip CI and break the audit trail.

---

## Releasing — promoting `dev` → `main`

When promoting changes from `dev` to `main` for a release:
- Each PR merged into `dev` creates a beta pre-release `v<version>-beta.<N>`.
- When an issue / PR is confirmed good and ready for release, it can be merged/promoted to `main` individually so unfinished issues or PRs on `dev` are not pushed to production before they are ready.

### Versioning rule (semver, beta pre-releases)

- While working on `dev`, each merged PR triggers a beta tag `v<version>-beta.<N>` (e.g. `v0.2.0-beta.1`, `v0.2.0-beta.2`). Timestamps are **not** used.
- **Before** opening the release PR, land a normal `chore/release-…` PR
  into `dev` that bumps `custom_components/ha_teams/manifest.json` to
  the target version:
  - `0.2.0-beta.*` → `0.2.0` (or next minor `0.3.0`)

  The release workflow reads the version from `manifest.json`, so the
  bump must already be on `dev` HEAD when the release PR is merged into
  `main`. Use the existing `chore/*` branch prefix — no new branch
  category is introduced for this step.
- **Major version bumps** (`0.x.y` → `1.0.0`, or later `1.x.y` → `2.0.0`) are reserved
  for breaking changes to the integration's user-facing config or entity model and
  must be discussed with the user first.

### Release PR checklist

1. On `dev`, bump `manifest.json` `version` to the next minor.
2. Commit: `chore(release): bump version to vX.Y.0` and push (via a normal
   PR to `dev` — never direct push).
3. Open release PR: `gh pr create --base main --head dev --title
   "release: vX.Y.0 — <summary>"`.
4. Wait for CI green and the Copilot review **submitted** (same gate as
   feature PRs).
5. Resolve any review comments.
6. **Merge with a merge commit** (`gh pr merge <N> --merge`), **never
   squash** — the dev PR history must be preserved on `main`.
7. Verify `release.yml` published a non-prerelease `vX.Y.0` GitHub
   Release.
8. **Immediately after releasing to `main`**: Bump `manifest.json` on `dev`
   to the next minor version (e.g. from `0.2.0` to `0.3.0`) via a `chore` PR on `dev`.
   This ensures subsequent beta builds on `dev` (e.g. `v0.3.0-beta.1`) have a higher
   version number than the stable release (e.g. `v0.2.0`) so HACS beta users receive updates.
   If any invalid post-release beta tags (matching the old version) were automatically
   created during the release PR merge, delete them using `gh release delete <tag> --yes --cleanup-tag`.

---

## Code Conventions

- **Language**: All code, comments, docstrings, commit messages, PR titles & descriptions, and GitHub issues MUST be in **English**. This applies even when the user/contributor communicates in another language — only the chat reply to the user may be in their language; everything that lands in the repository or on GitHub is English.
- **Python**: 3.12+, type hints required, `from __future__ import annotations` in every module.
- **Imports**: Use `from collections.abc import Callable` (not `from typing import Callable`).
- **Linter**: ruff — run `ruff check custom_components/` before committing.
- **Commit style**: Conventional Commits (`feat:`, `fix:`, `docs:`, `ci:`, `refactor:`).
- **Translations**: Add keys to `strings.json` first, then mirror to all `translations/*.json`.
- **No direct push to `main` or `dev`** — always use a PR.
- **Secrets**: Never store tokens, client secrets, or team/channel IDs directly in
  repository files; diagnostics must redact them (`diagnostics.py`).

---

## Known Issues / Quirks

- No official Teams Bot Transport (proactive bot messages, Adaptive Card actions),
  Activity Feed transport, or config subentries yet — these were deliberately deferred
  from an early architecture proposal (`voorstel.md`) to keep the initial scope small.
  See `C:\temp\skill-ha-teams.md` (local, not committed) for the full rationale.
- `tests/conftest.py` stubs the `homeassistant.*` modules instead of depending on the
  full `homeassistant` core package, so unit tests only cover pure logic (PKCE math,
  retry classification, Adaptive Card payload building) — not full config-flow/entity
  lifecycle behaviour. Consider `pytest-homeassistant-custom-component` for that.
