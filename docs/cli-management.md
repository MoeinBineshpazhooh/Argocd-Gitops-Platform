# CLI Management

The Argo CD CLI provides a scriptable interface for repository, application, synchronization, inspection, and account operations.

## Authentication

```bash
argocd login <ARGOCD_SERVER> \
  --username <USERNAME> \
  --password <PASSWORD>
```

Verify the current account:

```bash
argocd account get-user-info
```

## Repository management

Add the Git repository used by an Application:

```bash
argocd repo add https://gitlab.example.local/platform/my-app.git \
  --username <GITLAB_USERNAME> \
  --password <GITLAB_ACCESS_TOKEN>
```

List configured repositories:

```bash
argocd repo list
```

Get repository details:

```bash
argocd repo get https://gitlab.example.local/platform/my-app.git
```

Credentials are stored by Argo CD in its repository configuration. Do not put access tokens in manifests or shell scripts committed to Git.

## Create an application

```bash
argocd app create my-app \
  --repo https://gitlab.example.local/platform/my-app.git \
  --path manifests/workloads \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default \
  --project default \
  --revision main \
  --sync-policy automated \
  --self-heal \
  --auto-prune
```

This command establishes the relationship between the Git source and the Kubernetes destination.

## Inspect applications

List applications:

```bash
argocd app list
```

Inspect one application:

```bash
argocd app get my-app
```

View the desired/live difference:

```bash
argocd app diff my-app
```

View application history:

```bash
argocd app history my-app
```

## Synchronization

Manually synchronize:

```bash
argocd app sync my-app
```

Refresh the application's repository state:

```bash
argocd app get my-app --refresh
```

Wait for synchronization and health:

```bash
argocd app wait my-app --sync --health
```

## Troubleshooting from the CLI

Start with:

```bash
argocd app get my-app
argocd app diff my-app
argocd app history my-app
```

Then inspect Kubernetes resources:

```bash
kubectl get all -n default -l app=my-app
kubectl describe deployment my-app -n default
kubectl get events -n default --sort-by=.lastTimestamp
```

For controller/server-level problems:

```bash
kubectl get pods -n argocd
kubectl get events -n argocd --sort-by=.lastTimestamp
```

## Delete an application

```bash
argocd app delete my-app
```

Understand the deletion behavior before using destructive operations, especially when automated pruning or cascading deletion is enabled.

## CLI operational pattern

```text
LOGIN
  │
  ▼
REPOSITORY
  │
  ▼
APPLICATION
  │
  ├── GET / DIFF
  ├── SYNC
  ├── WAIT
  └── HISTORY
  │
  ▼
KUBERNETES VALIDATION
```

The CLI is especially useful for repeatable procedures and troubleshooting where a visual interface is not required.
