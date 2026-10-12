# Repository Security

Keep real GitLab tokens, SMTP credentials, private keys, local environment files and generated Secrets outside Git. The checked-in Secret examples intentionally contain fake values. Report a real exposure privately to the owner, revoke/rotate the credential first, and do not paste it into public issues or pull requests. Removing a file does not remove a leaked credential from Git history.

## Automated checks

`validate` checks YAML, local links and stage/production example policies. `secrets` uses a pinned Gitleaks action and engine with read-only permissions and redacted output. Each run checks the pushed/PR commit range, followed by an explicit scan of all fetched Git history. Automatic PR comments, report artifacts and summaries are disabled. Pattern scanning is not proof that all secrets are absent. Investigate findings and use narrow documented exceptions only for verified fake values.

Dependabot proposes weekly updates to GitHub Actions and Python dependencies when its configuration is merged. No automatic merge is configured. CI does not verify a running Kubernetes deployment or production RBAC.

The full-history scan identified one deliberately fake provider-shaped token in the original example Secret. Its historical file was checked against the documented fake value before adding one exact commit/file/rule/line fingerprint to `.gitleaksignore`. The current template uses a plain replacement marker. No entire path, provider rule or commit range is excluded.

## Proposed main protection

`.github/rulesets/main.json` is an importable proposal; a committed JSON file does not enable GitHub protection. It requires pull requests, up-to-date `validate` and `secrets` checks, resolved conversations, and blocks branch deletion and force pushes. Zero independent approvals supports a solo-maintainer workflow; add one when a second maintainer is available. No bypass actor is proposed.

At review on 2026-10-12, GitHub reported `main` unprotected. The ruleset read returned: upgrade to GitHub Pro or make this repository public. Private visibility is preserved. Activate the proposed ruleset through an administrator only after the GitHub account has an eligible private-repository plan and both check names have passed on main. The connected GitHub tools cannot write administration settings.

GitHub branch protection does not protect the external GitLab `devops` branch or authorize production Kubernetes sync. Configure protected release branches/tags in the actual GitLab source, least-privilege Argo CD RBAC, trusted repository TLS and secure credentials separately. Stage health is not release approval; follow the exact-revision procedure in [production approval](docs/production-approval.md).

Reference: [GitHub ruleset availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).
