# GitLab Integration

Argo CD can use a GitLab repository as the source of Kubernetes desired state.

## Repository model

```text
GitLab
  │
  │ Git repository
  ▼
Argo CD repository configuration
  │
  ▼
Application
  │
  ▼
Kubernetes
```

## Register a repository with the CLI

```bash
argocd repo add https://gitlab.example.local/platform/my-app.git \
  --username <GITLAB_USERNAME> \
  --password <GITLAB_ACCESS_TOKEN>
```

Use a credential with the minimum repository permissions required by the deployment model.

## Verify the repository

```bash
argocd repo list
argocd repo get https://gitlab.example.local/platform/my-app.git
```

The repository should report a successful connection before an Application is expected to synchronize from it.

## Application source

```yaml
source:
  repoURL: https://gitlab.example.local/platform/my-app.git
  path: manifests/workloads
  targetRevision: main
```

## Repository layout

A simple application repository can use:

```text
my-app/
├── manifests/
│   ├── deployment.yaml
│   └── service.yaml
└── README.md
```

Argo CD points the Application at `manifests/` or another directory containing the desired Kubernetes resources.

## Recommended Git workflow

```text
Developer
   │
   ▼
Feature branch
   │
   ▼
Merge request
   │
   ├── Review
   ├── Validation
   └── Approval
   │
   ▼
main
   │
   ▼
Argo CD
   │
   ▼
Kubernetes
```

This creates an auditable relationship between a Git revision and a deployed Kubernetes state.

## Authentication and secrets

Do not commit:

- GitLab passwords
- personal access tokens
- deploy tokens
- private SSH keys
- Argo CD repository Secret manifests containing credentials

The repository URL in this project is intentionally a placeholder:

```text
https://gitlab.example.local/platform/my-app.git
```

Replace it only in a deployment environment or local configuration where appropriate.

## Private GitLab / restricted environments

For an internal GitLab installation:

- ensure Argo CD can resolve the GitLab hostname
- ensure network connectivity from the Argo CD repository server
- provide a trusted CA when the GitLab certificate is internally signed
- use least-privilege repository credentials
- avoid public internet dependencies where the environment is isolated

## Troubleshooting

### Repository connection fails

Check:

```bash
argocd repo list
kubectl get pods -n argocd
```

Then validate DNS, network access, TLS trust, repository URL, and credential permissions from the Argo CD environment.

### Application cannot fetch manifests

Inspect:

```bash
argocd app get my-app
argocd app get my-app --refresh
```

Confirm that:

- the repository exists
- the configured revision exists
- the path exists
- the configured credentials can read the repository
- the Argo CD repository server is healthy
