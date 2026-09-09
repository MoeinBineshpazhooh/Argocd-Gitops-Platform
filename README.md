# Argo CD GitOps Platform

A production-oriented GitOps reference implementation for deploying and managing Kubernetes applications with Argo CD, Git-based desired state, automated reconciliation, and secure application delivery.

> **Portfolio note:** This repository is a sanitized, reproducible representation of hands-on Argo CD work. Internal hostnames, credentials, access tokens, certificates, and infrastructure-specific identifiers are intentionally replaced with placeholders.

## Overview

This project demonstrates a practical GitOps workflow in which Kubernetes application configuration is maintained in Git and Argo CD continuously compares the desired state with the live cluster state.

```text
                         Git repository
                              │
                              │ desired state
                              ▼
                        ┌───────────┐
                        │  Argo CD  │
                        │ Controller│
                        └─────┬─────┘
                              │
                    reconcile / sync
                              │
                              ▼
                    ┌─────────────────┐
                    │ Kubernetes      │
                    │ Cluster         │
                    └────────┬────────┘
                             │
                       running state
                             │
                             ▼
                    ┌─────────────────┐
                    │ Application     │
                    │ Workloads       │
                    └─────────────────┘
```

## What this repository demonstrates

- Argo CD installation on Kubernetes
- HTTPS exposure through an NGINX Ingress
- TLS configuration for the Argo CD endpoint
- Argo CD CLI installation and administration
- Argo CD web UI administration
- Git repository registration
- Kubernetes `Application` resources
- Application synchronization
- Automated synchronization
- Self-healing
- Automatic pruning
- Application health and sync-state inspection
- GitLab-backed GitOps workflows using sanitized example endpoints
- Private-registry and air-gapped deployment considerations
- Declarative application delivery using Kubernetes manifests

## GitOps workflow

The application source of truth is Git rather than a sequence of imperative `kubectl apply` operations.

```text
Developer / Operator
        │
        ▼
   Git repository
        │
        │ commit / merge
        ▼
     Argo CD
        │
        ├── Detect desired state
        ├── Compare with cluster
        ├── Calculate drift
        └── Synchronize resources
                │
                ▼
        Kubernetes cluster
```

When automated synchronization is enabled, Argo CD can reconcile changes without requiring an operator to run `kubectl apply` manually.

## Repository structure

```text
.
├── README.md
├── docs/
│   ├── architecture.md
│   ├── installation.md
│   ├── cli-management.md
│   ├── gui-management.md
│   ├── application-management.md
│   ├── gitlab-integration.md
│   ├── air-gapped.md
│   └── troubleshooting.md
├── manifests/
│   ├── argocd/
│   │   └── ingress.yaml
│   ├── applications/
│   │   └── my-app.yaml
│   └── workloads/
│       ├── deployment.yaml
│       └── service.yaml
└── examples/
    └── repository-layout.md
```

## Application example

The included demonstration application consists of a Kubernetes Deployment and Service stored under `manifests/workloads/`.

Argo CD manages these resources through an `Application` definition:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://gitlab.example.local/platform/my-app.git
    path: manifests/workloads
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Why these sync settings matter

| Setting | Purpose |
|---|---|
| `automated` | Allows Argo CD to synchronize detected Git changes automatically. |
| `prune` | Removes resources that are no longer defined in Git. |
| `selfHeal` | Reconciles supported out-of-band changes made directly in the cluster. |

Together, these settings implement a strong declarative reconciliation model.

## Documentation

| Guide | Purpose |
|---|---|
| [Architecture](docs/architecture.md) | Components, responsibilities, and GitOps flow |
| [Installation](docs/installation.md) | Install and expose Argo CD |
| [CLI Management](docs/cli-management.md) | Manage repositories and applications with `argocd` |
| [GUI Management](docs/gui-management.md) | Manage Argo CD through the web interface |
| [Application Management](docs/application-management.md) | Application lifecycle, sync, drift, health, and pruning |
| [GitLab Integration](docs/gitlab-integration.md) | Connect Argo CD to a Git repository |
| [Air-Gapped Deployment](docs/air-gapped.md) | Offline/private-registry considerations |
| [Troubleshooting](docs/troubleshooting.md) | Common operational checks and failures |

## CLI vs GUI

Both management paths are intentionally documented.

### CLI

The CLI is useful for repeatable administration, automation, troubleshooting, and operational workflows.

```bash
argocd app list
argocd app get my-app
argocd app sync my-app
argocd app delete my-app
```

### GUI

The web UI is useful for visual inspection and day-to-day operations such as:

- Application health
- Sync status
- Resource trees
- Git revision
- Differences between desired and live state
- Manual synchronization
- Application history
- Repository configuration

See the dedicated [GUI Management](docs/gui-management.md) guide.

## Security principles

This repository deliberately does **not** contain:

- passwords
- personal access tokens
- private keys
- TLS private keys
- internal credentials
- production secrets
- real internal repository addresses

Use placeholders such as:

```text
<ARGOCD_SERVER>
<GITLAB_USERNAME>
<GITLAB_ACCESS_TOKEN>
<TLS_CERTIFICATE_PATH>
<TLS_PRIVATE_KEY_PATH>
```

Secrets should be supplied through the appropriate secret-management mechanism in the target environment rather than committed to Git.

## Air-gapped / private infrastructure

Argo CD can be operated in environments where public internet access is restricted. The deployment model should account for:

1. Preparing required Argo CD images before the environment is isolated.
2. Mirroring required images into an approved private registry.
3. Ensuring Kubernetes nodes can pull from the private registry.
4. Making Git repositories reachable from the cluster or providing an approved internal Git service.
5. Avoiding runtime dependencies on public URLs.
6. Versioning installation manifests and image inventories for repeatability.

The [Air-Gapped Deployment](docs/air-gapped.md) guide documents the operational pattern without exposing environment-specific details.

## Design goals

This repository is intentionally focused on **operational understanding**, not simply installing Argo CD.

The target outcome is an operator who can explain and demonstrate:

- how Git becomes the desired state
- how Argo CD discovers and compares state
- how synchronization changes the cluster
- how drift is detected and corrected
- how applications are administered from both CLI and GUI
- how Git repositories are connected securely
- how the same model can be adapted to restricted or air-gapped environments

## Validation checklist

After deployment, validate at minimum:

```bash
kubectl get pods -n argocd
kubectl get ingress -n argocd
kubectl get applications -n argocd

argocd app list
argocd app get my-app
argocd app sync my-app
```

Expected application state:

```text
Sync Status:   Synced
Health Status: Healthy
```

## Portfolio positioning

This project demonstrates practical experience with **Kubernetes application delivery, GitOps, Argo CD, GitLab integration, declarative manifests, automated reconciliation, and operational troubleshooting**.

It complements Kubernetes infrastructure, networking, observability, CI/CD, and air-gapped platform projects by covering the application-delivery layer of a modern Kubernetes platform.

## License

This repository is provided as a technical portfolio and learning reference. Adapt the manifests and procedures to the security, networking, and operational requirements of your own environment.
