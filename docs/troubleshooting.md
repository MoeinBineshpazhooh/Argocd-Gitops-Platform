# Troubleshooting

## 1. Argo CD pods are not ready

```bash
kubectl get pods -n argocd
kubectl get events -n argocd --sort-by=.lastTimestamp
```

Inspect a specific pod:

```bash
kubectl describe pod <POD_NAME> -n argocd
```

Look for image-pull errors, scheduling problems, missing configuration, certificate problems, or resource constraints.

## 2. Argo CD UI is unreachable

Check:

```bash
kubectl get ingress -n argocd
kubectl get svc -n argocd
kubectl get pods -n argocd
```

Validate:

- DNS resolves to the expected ingress endpoint.
- NGINX Ingress Controller is healthy.
- TLS Secret exists.
- The Ingress hostname matches the certificate.
- Network policy/firewall rules permit access.

## 3. TLS problems

Inspect the Secret metadata:

```bash
kubectl get secret argocd-tls -n argocd
```

Do not print or commit the private key.

Confirm the certificate covers the configured hostname and is trusted by the client.

## 4. Repository connection failure

```bash
argocd repo list
```

Check the repository server:

```bash
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-repo-server
```

For private Git servers, verify DNS, network reachability, TLS trust, and credential permissions.

## 5. Application is OutOfSync

```bash
argocd app get my-app
argocd app diff my-app
```

Determine whether the difference is:

- an intended Git change
- an out-of-band Kubernetes change
- a generated/defaulted field
- an incorrect manifest
- an unexpected controller mutation

Do not blindly sync until the difference is understood.

## 6. Application is unhealthy

Start with:

```bash
argocd app get my-app
kubectl get all -n default -l app=my-app
kubectl get events -n default --sort-by=.lastTimestamp
```

Then inspect the affected Deployment, Pod, Service, or other resource.

## 7. Automated sync does not occur

Check:

```bash
argocd app get my-app
```

Verify that automated sync is configured:

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
```

Also verify that Argo CD can reach the Git repository and that the tracked revision changed as expected.

## 8. Self-healing appears not to work

Confirm:

- `selfHeal: true` is configured.
- The resource is managed by the Application.
- The observed change is a difference Argo CD can reconcile.
- The Application is not suspended or otherwise prevented from syncing.
- The Argo CD application controller is healthy.

## 9. Images cannot be pulled in an isolated environment

Inspect the Pod:

```bash
kubectl describe pod <POD_NAME> -n <NAMESPACE>
```

Check for:

- public image references
- incorrect private registry hostname
- missing image mirror
- registry TLS trust problems
- registry authentication issues
- network connectivity from the node

## Troubleshooting philosophy

Use Argo CD to understand desired/live state and Kubernetes tools to understand the actual workload/runtime failure.

```text
Argo CD
  │
  ├── Git source
  ├── Diff
  ├── Sync status
  └── Health
       │
       ▼
Kubernetes
  │
  ├── Pods
  ├── Events
  ├── Conditions
  └── Logs
```
