# Repository Validation

Run from the repository root with Python 3.12 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-validation.txt
python scripts/validate.py
```

GitHub Actions runs the same command for pushes and pull requests with read-only repository permissions. It does not connect to GitLab, Argo CD or Kubernetes, and needs no deployment credentials.

The validator checks:

- YAML parsing and duplicate mapping keys, including the workflow.
- Required resource identity fields in example manifests.
- Local inline Markdown file links outside code fences and unsupported chat rendering markup.
- Automatic stage synchronization with pruning and self-healing.
- Absence of automated production synchronization.
- The documented mapping from external GitLab source paths to the environment examples.

These checks do not validate full Kubernetes/Argo CD schemas, external links, heading anchors, RBAC enforcement, ingress behavior or runtime application health. Before using examples in a cluster, replace placeholders, validate against the installed CRDs, review the diff, and run smoke tests in stage.
