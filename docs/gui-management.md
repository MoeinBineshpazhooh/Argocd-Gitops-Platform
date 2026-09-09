# GUI Management

The Argo CD web interface provides a visual operational view of applications, synchronization state, resource health, history, and repository configuration.

## Access

Open the configured Argo CD HTTPS endpoint:

```text
https://<ARGOCD_SERVER>
```

Authenticate with an approved Argo CD account or the configured identity provider.

## Applications view

The Applications page provides a high-level view of managed workloads.

Typical information includes:

- Application name
- Project
- Sync status
- Health status
- Repository revision
- Destination cluster
- Destination namespace
- Automated synchronization state

A healthy application should normally show both a synchronized state and healthy resources after a successful deployment.

## Application details

Selecting an application opens its resource tree.

```text
Application
│
├── Deployment
│    └── ReplicaSet
│         └── Pods
│
└── Service
```

This view is useful for understanding which Kubernetes objects belong to the Application and where a deployment is failing.

## Sync operation

The GUI can be used to manually synchronize an application.

Typical workflow:

1. Open **Applications**.
2. Select the application.
3. Review the displayed sync status and resource changes.
4. Open the synchronization action.
5. Review the proposed resources.
6. Start synchronization.
7. Monitor resource health until the application reaches the expected state.

When automated synchronization is enabled, manual synchronization is normally needed only for operational control, testing, or recovery scenarios.

## Refresh and drift inspection

Refresh the application to make Argo CD evaluate the current repository/live state.

When drift exists, the UI can be used to inspect which resources differ from the desired configuration.

A useful investigation sequence is:

```text
Application
   │
   ├── Sync Status
   │
   ├── Diff
   │
   ├── Resource Tree
   │
   └── Events / Conditions
```

## Application history

The application history view helps operators identify repository revisions and synchronization events associated with deployments.

This is useful when investigating questions such as:

- Which Git revision was deployed?
- When did the application become unhealthy?
- Which synchronization preceded a failure?
- Which revision should be compared with the current state?

## Repository management

Repositories can be managed from the Argo CD settings area when the authenticated account has sufficient permissions.

The repository configuration should use:

- Approved Git server endpoint
- Appropriate authentication method
- Least-privilege credentials
- TLS verification where supported and required

Do not enter production credentials into screenshots, documentation, or example files committed to this repository.

## Projects

Argo CD Projects can be used to establish boundaries around:

- permitted source repositories
- permitted destination clusters/namespaces
- allowed resource types
- project roles and access

The sample uses the `default` project for simplicity. A production platform should normally define projects around application ownership and security boundaries.

## GUI troubleshooting workflow

When an application is unhealthy:

1. Check **Sync Status**.
2. Check **Health Status**.
3. Open the resource tree.
4. Identify the unhealthy resource.
5. Inspect resource conditions/events.
6. Compare desired and live state.
7. Validate the corresponding Kubernetes resource with `kubectl`.
8. Check Argo CD controller/server pod health if the problem appears systemic.

## CLI and GUI relationship

The GUI and CLI are two interfaces to the same Argo CD control plane.

```text
                 Argo CD control plane
                    /          \
                   /            \
                CLI              GUI
                 │                 │
                 └──────┬──────────┘
                        ▼
                 Applications
                        │
                        ▼
                   Kubernetes
```

The CLI is preferable for repeatability and automation; the GUI is particularly effective for visual inspection, resource trees, synchronization review, and interactive troubleshooting.
