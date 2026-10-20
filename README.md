# security-templates

Reusable DevSecOps pipeline and CI/CD security standard for engineering teams.

Security owns **one** pipeline template. Teams adopt it with about ten lines of YAML instead of
copying scanners into every repository, so every repo gets the same checks, the same gates
and the same reporting, and improvements reach every team at once.

## What it checks

| Stage | Catches | Tool |
|---|---|---|
| Secrets | Keys, tokens and passwords in code or git history | Gitleaks |
| SAST | Injection, unsafe code patterns | Semgrep |
| SCA | Known CVEs in dependencies | Trivy |
| IaC | Misconfigured Terraform, Kubernetes, Dockerfiles | Trivy |
| Container | Vulnerable packages in the built image | Trivy |

All results are uploaded as SARIF to the repository's **Security → Code scanning** tab.
High and Critical findings (with a fix available) and any secret fail the build when
`enforce: true`.

## Adopt it in your repo

Add `.github/workflows/security.yml`:

```yaml
name: security
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
  security-events: write
jobs:
  devsecops:
    uses: YOUR-GITHUB-USERNAME/security-templates/.github/workflows/devsecops-reusable.yml@v1
    with:
      container-scan: true          # build and scan your image
      dockerfile: Dockerfile
      iac-path: infra/
      enforce: false                # report-only while you clear existing findings
```

### Inputs

| Input | Default | Purpose |
|---|---|---|
| `severity-threshold` | `HIGH,CRITICAL` | Severities that fail the build |
| `iac-path` | `.` | Folder with Terraform / K8s / Dockerfiles |
| `container-scan` | `false` | Build and scan a container image |
| `dockerfile` | `Dockerfile` | Dockerfile path for the image scan |
| `enforce` | `true` | `false` = report only (onboarding mode) |

## Rollout model

1. **Onboard** with `enforce: false`: findings show in the Security tab, nothing is blocked.
2. **Clear** existing High/Critical findings or record approved exceptions.
3. **Enforce** (`enforce: true`, the default): new High/Critical issues and secrets block merges.

Rules, fix deadlines and the exception process are in
[docs/SECURITY-STANDARD.md](docs/SECURITY-STANDARD.md).

## Live demo

[`demo/`](demo/) is a deliberately insecure Flask app, Dockerfile and Terraform config.
The [`self-test`](.github/workflows/self-test.yml) workflow runs the template against it on every
push, in report-only mode, so the findings are visible in this repo's Security tab.
**Never deploy anything in `demo/`.**

## Versioning

Teams pin a major version (`@v1`). Non-breaking improvements move the `v1` tag; breaking
changes (new blocking checks, stricter thresholds) ship as `v2` with an announced migration window.

## Repository layout

```
.github/workflows/devsecops-reusable.yml   the template
.github/workflows/self-test.yml            runs the template on demo/
examples/caller-example.yml                what a team adds to its repo
docs/SECURITY-STANDARD.md                  the standard behind the gates
demo/                                      deliberately vulnerable sample
```
