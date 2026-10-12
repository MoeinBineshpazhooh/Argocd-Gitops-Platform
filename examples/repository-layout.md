# Example GitOps Repository Layout

The current examples use separate stage and production directories so each Argo CD Application has an explicit environment boundary.

The `example-stage.yaml` and `example-production.yaml` Applications refer to an **external GitLab repository** and its `devops` branch. Their paths are relative to that repository's root:

| Application source path in GitLab | Sample files in this repository |
|---|---|
| `environments/stage` | `manifests/environments/stage/` |
| `environments/production` | `manifests/environments/production/` |

Copy the sample workload directories to those paths in the external repository, create the configured branch, and replace the placeholder repository URL and image reference before applying the Applications. If using this repository itself as the source, configure `repoURL`, `targetRevision` and the `manifests/environments/...` paths accordingly.

Apply only the configuration needed for your example. Do not apply all of `manifests/` recursively: it includes alternative Applications and fake Secret templates.

A small application repository can be organized as follows:

```text
my-app/
├── manifests/
│   ├── deployment.yaml
│   └── service.yaml
└── README.md
```

For a larger platform, environment overlays or a Helm/Kustomize structure can be introduced without changing the core Argo CD model.

Example:

```text
my-app/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    └── production/
        └── kustomization.yaml
```

The Argo CD `Application` should point to the directory that represents the intended deployment configuration.
