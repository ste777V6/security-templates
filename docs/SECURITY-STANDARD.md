# CI/CD Security Standard (v1)

**Applies to:** every repository that builds or deploys code.
**Owner:** Security · **Review:** every 6 months

## Why this exists

Most breaches start with something a pipeline could have caught: a leaked key, a
library with a known exploit, a public S3 bucket, an outdated base image. This
standard makes those checks automatic and identical across teams, so security is
part of every pull request instead of a review at the end.

## 1. Required checks

Every repo must call the central workflow `security-templates/devsecops-reusable.yml`
(pinned to a major version, e.g. `@v1`) on pull requests and on pushes to `main`.

| Check | What it catches | Tool |
|---|---|---|
| Secrets | API keys, passwords, tokens in code or git history | Gitleaks |
| SAST | Injection, unsafe deserialisation, weak crypto in our code | Semgrep |
| SCA | Known CVEs in third-party dependencies | Trivy |
| IaC | Misconfigured Terraform, Kubernetes, Dockerfiles | Trivy |
| Container | Vulnerable OS packages and libraries in images | Trivy (if the repo ships an image) |

Teams must not copy the scanners into their own workflows. Changes go through a
pull request to `security-templates`, so every team benefits.

## 2. Build gates

| Severity | Pull request | Merge to `main` |
|---|---|---|
| Critical / High (with a fix available) | Fails | Blocked |
| Any detected secret | Fails | Blocked |
| Medium | Reported in Security tab | Allowed, tracked |
| Low | Reported | Allowed |

New repositories start in **report-only mode** (`enforce: false`) for up to two
weeks to clear existing findings, then switch to enforced.

## 3. Remediation SLAs

| Severity | Fix within |
|---|---|
| Critical (or on CISA KEV) | 7 days |
| High | 30 days |
| Medium | 90 days |
| Low | Best effort |

A leaked secret is treated as an incident: **rotate it first**, then remove it
from the code. Deleting the commit is not enough.

## 4. Exceptions

False positives and accepted risks are allowed, but they must be visible:

- Suppress in code with an inline comment or `.trivyignore` entry that states
  the reason and the ticket number.
- Accepted risks need Security approval and an expiry date (max 90 days).
- Exceptions are reviewed monthly; expired ones fail the build again.

## 5. Baseline rules for engineers

- No secrets in code, config or CI variables in plain text; use the secrets manager.
- Pin dependency versions and container base images; prefer minimal / distroless images.
- Containers run as non-root.
- Terraform: encryption on, no public buckets or `0.0.0.0/0` admin ports,
  least-privilege IAM (no `*:*` policies).

## 6. Reporting

Results are in each repo's GitHub **Security** tab. Security publishes a monthly
summary per team: open findings by severity, SLA breaches and trend.
