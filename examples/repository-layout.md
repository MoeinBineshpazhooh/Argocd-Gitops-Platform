# Example GitOps Repository Layout

The current examples use separate stage and production directories so each Argo CD Application has an explicit environment boundary.

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
