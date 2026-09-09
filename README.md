<div align="center">
  <img src="https://github.com/MoeinBineshpazhooh.png?size=160" width="120" alt="Moein Bineshpazhooh" />
  <h1>🚀 Argo CD GitOps Platform</h1>
  <p><strong>Argo CD • GitOps • Kubernetes • GitLab • Automated Reconciliation • CLI • GUI • Air-Gapped</strong></p>
</div>

<div align="center">

![Argo CD](https://img.shields.io/badge/Argo%20CD-GitOps-EF7B4D?logo=argo&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Deployment-326CE5?logo=kubernetes&logoColor=white)
![GitOps](https://img.shields.io/badge/GitOps-Declarative-111827)
![GitLab](https://img.shields.io/badge/GitLab-Repository-FC6D26?logo=gitlab&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-Ingress-009639?logo=nginx&logoColor=white)
![TLS](https://img.shields.io/badge/TLS-HTTPS-6B7280)
![Air--Gapped](https://img.shields.io/badge/Environment-Air--Gapped-111827)

</div>

> **Portfolio case study:** this repository demonstrates the practical deployment and operation of Argo CD as a GitOps delivery layer for Kubernetes, including Git-based application management, automated reconciliation, CLI and GUI operations, HTTPS exposure, private Git integration, and restricted-environment considerations.

## 🎯 What I Actually Implemented

- Installed and configured **Argo CD** inside Kubernetes.
- Exposed the Argo CD server through **NGINX Ingress** with HTTPS/TLS.
- Configured an Argo CD endpoint using a Kubernetes TLS secret.
- Installed and used the **Argo CD CLI** for day-to-day administration.
- Managed Argo CD through both the **CLI and web GUI**.
- Registered a GitLab repository as an Argo CD application source.
- Created Kubernetes applications using the Argo CD `Application` resource.
- Deployed Kubernetes manifests from Git rather than relying on imperative application deployment.
- Enabled automated synchronization of desired state.
- Enabled **self-healing** to reconcile supported out-of-band changes.
- Enabled **automatic pruning** so resources removed from Git can be removed from the cluster.
- Inspected application health, synchronization state and resource status.
- Performed manual synchronization and application lifecycle operations.
- Documented private Git repository and restricted / **air-gapped** deployment considerations.
- Sanitized environment-specific addresses, credentials, certificates and access tokens for portfolio publication.

image_group{"layout":"carousel","aspect_ratio":"16:9","query":["Argo CD GitOps architecture Kubernetes","Argo CD application dashboard Kubernetes","GitOps Argo CD deployment workflow"],"num_per_query":1}

## 🏗️ GitOps Delivery Lifecycle

```text
Developer / Operator
        ↓
   Git Repository
        ↓
   Desired State
        ↓
      Argo CD
        ↓
  Compare / Detect Drift
        ↓
      Sync / Reconcile
        ↓
 Kubernetes Cluster
        ↓
 Running Application
```

The key principle is that **Git becomes the declarative source of truth**. Argo CD continuously evaluates the desired state stored in Git against the live Kubernetes state and reconciles the application when synchronization is configured.

## 🧭 Platform Architecture

```text
                         GitLab
                    Git Repository
                          │
                          │ manifests
                          ▼
                 ┌──────────────────┐
                 │     Argo CD      │
                 │                  │
                 │ Application      │
                 │ Controller       │
                 │ Repo Server      │
                 │ API / UI Server  │
                 └────────┬─────────┘
                          │
                   Sync / Reconcile
                          │
                          ▼
                 ┌──────────────────┐
                 │    Kubernetes    │
                 │     Cluster     │
                 └────────┬─────────┘
                          │
                    Application
                    Resources
```

### External Access

```text
User / Operator
       │
       ▼
 argocd.example.com
       │
       ▼
 NGINX Ingress
       │
       │ HTTPS
       ▼
 Argo CD Server
       │
       ├── Web GUI
       └── CLI / API
```

## 📋 Platform Capability Matrix

| Area | Implementation |
|---|---|
| GitOps Engine | Argo CD |
| Target Platform | Kubernetes |
| Source Repository | GitLab / Git repository |
| Application Definition | Argo CD `Application` |
| Deployment Model | Declarative GitOps |
| Synchronization | Automated / Manual |
| Drift Handling | Self-heal |
| Resource Cleanup | Automatic pruning |
| Web Access | NGINX Ingress |
| Transport Security | HTTPS / TLS |
| Administration | Argo CD CLI + Web GUI |
| Application Source | Kubernetes manifests |
| Environment Model | Private / restricted capable |
| Credentials | Externalized / sanitized |

## 🔬 GitOps Reconciliation Model

The repository follows the operational loop:

```text
Git Change
    ↓
Argo CD Detection
    ↓
Desired vs Live Comparison
    ↓
OutOfSync Detection
    ↓
Synchronization
    ↓
Kubernetes Resource Update
    ↓
Health Evaluation
    ↓
Continuous Reconciliation
```

This is intentionally different from a deployment process based only on `kubectl apply`. The deployment intent is persisted in Git and continuously reconciled by Argo CD.

## 🔄 Automated Synchronization

The demonstration `Application` uses:

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
```

### `automated`

Allows Argo CD to synchronize changes detected in the configured Git source without requiring an operator to manually execute a sync operation.

### `selfHeal`

Allows Argo CD to reconcile supported changes made directly against managed Kubernetes resources, restoring the state represented by Git.

### `prune`

Allows Argo CD to remove managed resources that are no longer declared by the desired state.

Together these capabilities establish the core **continuous reconciliation** model demonstrated by this project.

## 🖥️ CLI Management

The CLI workflow is documented as an operational management path rather than only an installation command.

```text
Install CLI
    ↓
Authenticate
    ↓
Register Repository
    ↓
Create Application
    ↓
Inspect Status
    ↓
Sync / Reconcile
    ↓
Troubleshoot
    ↓
Lifecycle Management
```

Typical operations include:

```bash
argocd app list
argocd app get my-app
argocd app sync my-app
argocd app delete my-app
```

The dedicated [`docs/cli-management.md`](docs/cli-management.md) guide covers authentication, repository management, application operations, synchronization and troubleshooting.

## 🖥️ GUI Management

The Argo CD web interface provides visual application operations and is documented as a separate management workflow.

```text
Argo CD GUI
    │
    ├── Applications
    │      ├── Sync Status
    │      ├── Health Status
    │      ├── Resource Tree
    │      ├── Git Revision
    │      ├── Diff
    │      └── History
    │
    ├── Projects
    └── Repositories
```

The GUI workflow is useful for quickly understanding application state, investigating synchronization problems and performing controlled manual operations.

See [`docs/gui-management.md`](docs/gui-management.md).

## 📦 Application Model

A managed application is represented declaratively with an Argo CD `Application` resource.

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

The important relationship is:

```text
Application
    │
    ├── source.repoURL
    ├── source.path
    ├── source.targetRevision
    │
    └── destination
             │
             ▼
       Kubernetes Cluster
```

## 🔗 GitLab Integration

The demonstrated workflow connects Argo CD to a private Git repository and uses the repository as the application source.

```text
GitLab Repository
       │
       │ manifests
       ▼
    Argo CD
       │
       │ reconcile
       ▼
 Kubernetes
```

Repository credentials are intentionally represented using placeholders and must never be committed to the portfolio repository.

Example:

```bash
argocd repo add https://gitlab.example.local/platform/my-app.git \
  --username <GITLAB_USERNAME> \
  --password <GITLAB_ACCESS_TOKEN>
```

See [`docs/gitlab-integration.md`](docs/gitlab-integration.md).

## 🧩 Example Workload

The repository contains a small Kubernetes workload used to demonstrate the complete GitOps path:

```text
manifests/workloads/
├── deployment.yaml
└── service.yaml
```

The example Deployment uses multiple replicas and the Service exposes the workload internally through `ClusterIP`.

The example is intentionally simple: the focus is the **delivery and reconciliation mechanism**, not application complexity.

## 🔐 Security Model

The repository follows a strict separation between configuration and sensitive credentials.

### Never commit

- Passwords
- Personal access tokens
- Private keys
- TLS private keys
- Production secrets
- Internal credentials
- Real infrastructure access details

### Use placeholders

```text
<ARGOCD_SERVER>
<GITLAB_USERNAME>
<GITLAB_ACCESS_TOKEN>
<TLS_CERTIFICATE_PATH>
<TLS_PRIVATE_KEY_PATH>
```

The actual environment should provide secrets through an appropriate secure mechanism rather than embedding them in Git.

## 📴 Restricted / Air-Gapped Operations

Argo CD operation in restricted environments requires dependencies to be prepared before isolation.

```text
Online Preparation
       ↓
Argo CD Images + Manifests + CLI
       ↓
Private Registry / Offline Transfer
       ↓
Restricted Kubernetes Environment
       ↓
Internal Git Repository
       ↓
Argo CD
       ↓
GitOps Reconciliation
```

The air-gapped documentation focuses on the operational model:

- Pre-stage required Argo CD container images.
- Mirror images into an approved private registry.
- Ensure Kubernetes nodes can pull required images.
- Make the Git repository reachable through an internal network path.
- Avoid runtime dependencies on public endpoints.
- Version installation manifests and image inventories.
- Keep environment-specific credentials outside the repository.

See [`docs/air-gapped.md`](docs/air-gapped.md).

## 🧯 Troubleshooting Philosophy

Troubleshooting follows the GitOps control path instead of immediately changing Kubernetes resources manually.

```text
Git Repository
      ↓
Repository Connectivity
      ↓
Argo CD Application
      ↓
Desired / Live Comparison
      ↓
Sync Status
      ↓
Resource Health
      ↓
Kubernetes Events / Logs
      ↓
Recovery / Reconciliation
```

Typical operational questions include:

- Is the repository reachable from Argo CD?
- Is the application `Synced` or `OutOfSync`?
- Is the application `Healthy`?
- Is the desired manifest different from the live resource?
- Did synchronization fail?
- Are required images available in the target registry?
- Is the destination namespace available?
- Is the Argo CD server reachable through the Ingress?

See [`docs/troubleshooting.md`](docs/troubleshooting.md).

## 📚 Operational Runbook

The repository documentation is organized around the complete lifecycle:

1. Install Argo CD.
2. Configure external HTTPS access.
3. Authenticate through CLI or GUI.
4. Register the Git repository.
5. Define the Argo CD application.
6. Deploy Kubernetes manifests from Git.
7. Inspect synchronization and health.
8. Perform manual or automated synchronization.
9. Validate self-healing and pruning behavior.
10. Troubleshoot repository, synchronization and workload failures.
11. Apply the same GitOps model to restricted environments.

## 📁 Repository Structure

```text
Argocd-Gitops-Platform/
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

## 🔗 Position in the Portfolio

```text
ON-PREM KUBERNETES FOUNDATION
              ↓
       KUBERNETES PLATFORM
              │
     ┌────────┼─────────┐
     ↓        ↓         ↓
 Networking  Storage  Observability
     │        │         │
     └────────┼─────────┘
              ↓
          CI / CD
              ↓
         GitOps / Argo CD
              ↓
     APPLICATION DELIVERY
              ↓
      PRODUCTION OPERATIONS
```

This repository represents the **GitOps and application-delivery layer** of the broader Kubernetes platform portfolio.

## 🧭 Engineering Principles

- **Git as the source of truth:** desired application state is versioned and reviewable.
- **Declarative delivery:** Kubernetes resources are delivered from Git rather than maintained through ad-hoc commands.
- **Continuous reconciliation:** detect drift and continuously converge toward the desired state.
- **Operational visibility:** provide both CLI and GUI management paths.
- **Secure by default:** never publish credentials or production secrets.
- **Repeatable:** keep manifests and operational procedures version controlled.
- **Offline-aware:** avoid assuming unrestricted internet connectivity.
- **Recoverable:** use health, sync state and reconciliation behavior as operational signals.

## 🚦Project Scope

This repository intentionally focuses on the Argo CD GitOps delivery layer demonstrated through the sample implementation.

It does **not** claim that every advanced Argo CD capability is implemented. Features such as complex multi-cluster ApplicationSets, progressive delivery, external secret management and advanced RBAC can be introduced as separate extensions when actually implemented and validated.

<div align="center">

### 📦 Git → 🔄 Reconcile → ☸️ Deploy → 🔍 Observe → 🛠️ Operate

<strong>Practical Argo CD GitOps application delivery for Kubernetes environments.</strong>

</div>
