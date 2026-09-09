# Air-Gapped Deployment Considerations

Argo CD itself does not remove the operational challenges of running GitOps in an isolated environment. The required container images, manifests, CLI binaries, Git service, certificates, and dependencies must be available through approved internal infrastructure.

## Reference architecture

```text
             Pre-isolation preparation
                      │
          ┌───────────┴───────────┐
          │                       │
    Argo CD images           CLI binary
          │                       │
          └───────────┬───────────┘
                      ▼
             Private registry
                      │
                      ▼
             Air-gapped cluster
                      │
                      ▼
                   Argo CD
                      │
                      ▼
             Internal Git server
```

## Preparation workflow

1. Select and pin the Argo CD release.
2. Download the installation manifests before isolation.
3. Identify every container image referenced by the selected manifests.
4. Pull and verify the required images.
5. Push approved images to the private registry.
6. Prepare the Argo CD CLI binary for operator workstations.
7. Make the Git repository available through the internal Git service.
8. Configure internal CA trust where required.
9. Test installation and synchronization before final isolation.

## Image inventory

Maintain an inventory similar to:

```text
Component                  Image                                      Version
---------                  -----                                      -------
Argo CD API server         <PRIVATE_REGISTRY>/argocd-server            <VERSION>
Argo CD repo server        <PRIVATE_REGISTRY>/argocd-repo-server       <VERSION>
Argo CD controller         <PRIVATE_REGISTRY>/argocd-application-controller <VERSION>
Redis / dependency         <PRIVATE_REGISTRY>/<DEPENDENCY>             <VERSION>
```

The exact image set depends on the selected Argo CD release and installation manifest. Generate the inventory from the exact version being deployed rather than copying an outdated list.

## Private registry considerations

The Kubernetes nodes must be able to pull the mirrored images from the approved registry.

If the registry uses a private CA, install the CA trust chain according to the container runtime and cluster security model.

Do not put registry credentials into this repository.

## Git repository considerations

The Git source must be reachable from the Argo CD repository server without public internet access.

Example sanitized source:

```text
https://gitlab.example.local/platform/my-app.git
```

For an internal GitLab deployment, validate:

- DNS resolution
- routing
- firewall policy
- TLS trust
- repository authentication
- repository permissions

## Avoid public runtime dependencies

A common mistake is to install an application successfully while leaving a later runtime dependency on a public URL.

For isolated environments, review:

- container images
- Helm charts
- Git repositories
- CA certificates
- CLI binaries
- admission/webhook images
- sidecars and init containers
- image pull policies

## Operational principle

```text
Everything required at runtime
              │
              ▼
      Must exist internally
              │
       ┌──────┴──────┐
       ▼             ▼
 Private Git     Private Registry
       │             │
       └──────┬──────┘
              ▼
           Argo CD
              │
              ▼
        Kubernetes
```

## Validation checklist

- [ ] Argo CD release is pinned
- [ ] Installation manifests are archived
- [ ] Required images are inventoried
- [ ] Images are mirrored to the private registry
- [ ] Image pulls work from Kubernetes nodes
- [ ] Internal Git repository is reachable
- [ ] Internal CA trust is configured
- [ ] CLI binary is available offline
- [ ] Application manifests contain no public image references
- [ ] Application synchronization works without public internet
