# Application Management

## Application lifecycle

This repository demonstrates two application policies: automated reconciliation for stage and explicit synchronization for production.

A typical Argo CD Application lifecycle is:

```text
Create
  │
  ▼
Discover source
  │
  ▼
Compare desired/live state
  │
  ├── Synced ───────────────┐
  │                         │
  └── OutOfSync             │
           │                │
           ▼                │
         Sync               │
           │                │
           ▼                │
         Health             │
           │                │
           └──────► Healthy ┘
```

## Application manifest

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: example-app-stage
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://gitlab.example.local/platform/example-gitops.git
    path: environments/stage
    targetRevision: devops
  destination:
    server: https://kubernetes.default.svc
    namespace: example-stage
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Source configuration

The `source` block identifies:

- `repoURL`: Git repository
- `path`: directory containing the manifests
- `targetRevision`: branch, tag, or commit to track

For controlled production deployments, pinning a release/tag or using a controlled branch strategy can reduce unexpected changes.

## Destination configuration

The `destination` block identifies where the resources are deployed.

For an Argo CD instance managing the same Kubernetes cluster:

```yaml
destination:
  server: https://kubernetes.default.svc
  namespace: default
```

## Automated synchronization

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
```

### Automated sync

Argo CD can apply changes detected in the configured Git revision.

### Pruning

Pruning removes resources that were previously managed but are no longer part of the desired state.

This is powerful and should be enabled only when the repository is treated as the authoritative desired state.

### Self-healing

Self-healing allows Argo CD to correct supported changes made directly to live resources when they differ from Git.

This reinforces the principle that Git is the desired-state source of truth.

## Manual sync

Even with automated synchronization, operators may use manual sync during controlled testing or recovery:

```bash
argocd app sync my-app
```

## Application states

### Synced

The live resources correspond to the desired state represented by the configured source revision.

### OutOfSync

A difference exists between the desired state and the observed live state.

Investigate the diff before deciding whether synchronization is appropriate.

### Healthy

Argo CD health assessment indicates that the application's resources meet their health criteria.

### Degraded

One or more resources are not meeting the expected health condition. Inspect the resource tree, conditions, events, and Kubernetes workload status.

## Safe operational workflow

```text
Git change
   │
   ▼
Review change
   │
   ▼
Argo CD detects revision
   │
   ▼
Review diff
   │
   ▼
Sync
   │
   ▼
Check health
   │
   ▼
Validate application
```

## Avoiding configuration drift

Direct `kubectl edit`, `kubectl patch`, or imperative changes can create temporary state that is not represented in Git. With self-healing enabled, Argo CD may later reconcile those changes.

The preferred approach is to change the desired configuration in Git, review it, and allow Argo CD to reconcile the cluster.

## Deletion

CLI example:

```bash
argocd app delete my-app
```

Application deletion should be treated as a potentially destructive operation. Understand the application's resource deletion policy before performing it in a production environment.
