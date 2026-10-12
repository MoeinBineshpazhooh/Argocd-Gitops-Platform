# Installation

This guide installs Argo CD into a Kubernetes cluster and exposes the Argo CD server through an HAProxy Ingress with TLS.

## Prerequisites

- Kubernetes cluster with `kubectl` access
- HAProxy Ingress Controller
- DNS record for the Argo CD hostname
- TLS certificate and private key for that hostname
- Network access to the Argo CD manifests, or a prepared offline copy for restricted environments

## 1. Create the namespace

```bash
kubectl create namespace argocd
```

## 2. Install Argo CD

For an environment with internet access, use the official installation manifest for the selected Argo CD release.

```bash
kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

For production use, pin a tested Argo CD release instead of relying on a moving `stable` reference.

### Offline installation

In an air-gapped environment, download and review the required installation manifests before isolation, mirror all required container images into the approved private registry, and apply a controlled local copy of the manifests.

See [Air-Gapped Deployment](air-gapped.md).

## 3. Validate the installation

```bash
kubectl get pods -n argocd
kubectl get svc -n argocd
```

Wait until the Argo CD components required for the server and controllers are ready.

## 4. Create the TLS secret

Prepare the certificate and key through your organization's secure certificate-management process.

```bash
kubectl create secret tls argocd-tls \
  --cert=<TLS_CERTIFICATE_PATH> \
  --key=<TLS_PRIVATE_KEY_PATH> \
  -n argocd
```

Never commit the certificate private key or the generated Secret manifest to Git.

## 5. Configure the Ingress

Apply `manifests/argocd/ingress.yaml` after replacing the placeholder hostname with the target environment's DNS name.

The supplied manifest targets HAProxy Technologies' Kubernetes Ingress Controller with `ingressClassName: haproxy`. It terminates client TLS at the ingress and uses `haproxy.org/server-ssl: "true"` for TLS to the Argo CD server on port 443. Confirm the matching IngressClass exists and the server serves TLS. Configure backend CA trust according to your controller version; encryption alone does not establish backend certificate verification.

For controller-specific options and annotation behavior, see the [HAProxy Kubernetes Ingress Controller annotation reference](https://www.haproxy.com/documentation/kubernetes-ingress/community/configuration-reference/ingress/).

```bash
kubectl apply -f manifests/argocd/ingress.yaml
```

Verify:

```bash
kubectl get ingress -n argocd
kubectl describe ingress argocd-server-ingress -n argocd
```

## 6. Retrieve the initial admin password

The initial password is stored in the `argocd-initial-admin-secret` Secret.

```bash
kubectl get secret argocd-initial-admin-secret \
  -n argocd \
  -o jsonpath="{.data.password}" | base64 -d
```

Treat this value as a credential. Do not paste it into Git, tickets, documentation, or shell history when avoidable.

## 7. Change the admin password

After the first successful login, change the initial password:

```bash
argocd account update-password
```

For production environments, prefer named accounts, RBAC, and an enterprise identity provider where available instead of relying on the built-in administrator for routine operations.

## 8. Install the Argo CD CLI

For a controlled environment, obtain the CLI binary from the same approved release/version used by the platform and verify its checksum according to the release documentation.

Example installation pattern:

```bash
curl -sSL -o /usr/local/bin/argocd \
  https://github.com/argoproj/argo-cd/releases/download/<VERSION>/argocd-linux-amd64

chmod +x /usr/local/bin/argocd
```

In an air-gapped environment, transfer the previously approved binary rather than downloading it from the public internet.

## 9. Login

```bash
argocd login <ARGOCD_SERVER> \
  --username <USERNAME> \
  --password <PASSWORD>
```

If the environment uses a trusted certificate, do not disable TLS verification. The `--insecure` option should only be used when the security model explicitly requires it and the operator understands the consequences.

## 10. Verify

```bash
argocd version
argocd account get-user-info
argocd app list
```

## Installation checklist

- [ ] Namespace created
- [ ] Argo CD installed
- [ ] Pods healthy
- [ ] Ingress Controller available
- [ ] TLS Secret created securely
- [ ] Ingress configured
- [ ] DNS configured
- [ ] Initial password retrieved securely
- [ ] Initial password changed
- [ ] CLI installed and version aligned
- [ ] CLI login verified

## Notes for production

- Pin Argo CD versions.
- Review release compatibility with the Kubernetes version in use.
- Restrict access to the Argo CD endpoint.
- Use trusted TLS certificates.
- Avoid permanent use of the initial admin account.
- Store repository credentials securely.
- Maintain an offline image inventory when operating without internet access.
