# Architecture

## Purpose

This project uses Argo CD as the reconciliation layer between Kubernetes desired state in Git and live state in a Kubernetes cluster.

The example source is a private GitLab repository. Argo CD reaches GitLab over HTTPS from the repo-server; GitLab does not need an inbound Kubernetes API connection for repository consumption.

## High-level architecture

```text
                         ┌──────────────────────┐
                         │ Git repository       │
                         │ Kubernetes manifests  │
                         └──────────┬───────────┘
                                    │
                             Git revision
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Argo CD        │
                         │                      │
                         │ Application objects  │
                         │ Repo integration     │
                         │ Reconciliation       │
                         │ Sync / Health        │
                         └──────────┬───────────┘
                                    │
                             Kubernetes API
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Kubernetes cluster   │
                         │                      │
                         │ Deployment           │
                         │ Service              │
                         │ Other resources      │
                         └──────────────────────┘
```

## Core concepts

### Git repository

Git stores the declarative configuration that represents the desired application state. A commit to the configured branch becomes a new desired state for Argo CD to evaluate.

### Argo CD Application

An `Application` connects three things:

1. The source repository and revision.
2. The path containing Kubernetes configuration.
3. The destination Kubernetes cluster and namespace.

Example:

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
```

### Reconciliation

Argo CD continuously evaluates the difference between the desired state represented in Git and the live state observed in Kubernetes.

```text
Desired state                 Live state
     │                            │
     └──────────┐      ┌──────────┘
                ▼      ▼
             Argo CD comparison
                    │
          ┌─────────┴─────────┐
          │                   │
       No drift             Drift
          │                   │
       Healthy          Sync / repair
```

### Automated synchronization

The demonstration application enables:

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
```

`prune` removes resources that have been removed from the desired state. `selfHeal` allows Argo CD to reconcile supported out-of-band changes back toward the Git-defined state.

## Ingress architecture

The sample exposes the Argo CD server through an HAProxy Ingress with TLS.

```text
Client
  │ HTTPS
  ▼
HAProxy Ingress
  │ HTTPS to backend
  ▼
argocd-server :443
  │
  ▼
Argo CD services
```

The example deliberately uses a placeholder hostname and certificate secret. Replace them only in the target environment.

## Security boundaries

The repository separates:

- source configuration
- Kubernetes resources
- Argo CD application definitions
- credentials and certificates

Credentials are not stored in Git. Repository credentials and TLS private keys must be supplied securely at deployment time.

## Operational model

The current example separates stage validation from production rollout. Stage reconciles automatically; production remains OutOfSync until an operator reviews and synchronizes the approved revision.

The intended operational model is:

```text
Change desired state in Git
          │
          ▼
      Review / merge
          │
          ▼
       Argo CD
          │
          ▼
   Detect new revision
          │
          ▼
     Compare state
          │
          ▼
      Synchronize
          │
          ▼
      Kubernetes
          │
          ▼
  Health / sync verification
```

This keeps application delivery auditable and makes Git the central source of truth.
