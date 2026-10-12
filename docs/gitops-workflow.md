# GitOps Deployment Workflow

## End-to-end flow

~~~text
Developer
   |
   v
Application Git repository
   |
   | CI build / test / image
   v
Container Registry
   |
   | image tag
   v
GitOps manifest update
   |
   v
Protected devops branch
   |
   v
Argo CD
   |-------------------|
   v                   v
Stage               Production
auto sync           manual sync
   |                   |
   v                   v
Kubernetes        Kubernetes
~~~

The GitOps repository contains the desired Kubernetes state. Argo CD pulls that state and reconciles the target cluster.

## Network model

~~~text
Argo CD repo-server
       |
       | HTTPS / TCP 443
       v
     GitLab

GitLab CI -------- X --------> Kubernetes API
       no direct deployment dependency
~~~

The exact network policy depends on the environment. The important separation is that Argo CD performs the Kubernetes reconciliation.

## Stage

Stage is the validation environment.

- Git revision: devops
- Automated sync: enabled
- Self-heal: enabled
- Pruning: enabled
- Namespace: example-stage

A successful stage synchronization and healthy resources are prerequisites for validation. Run application smoke/integration tests and approve the exact Git commit and image artifacts before production synchronization. See [Production Approval](production-approval.md).

## Production

Production uses the same desired-state model but does not enable automated synchronization in the example.

~~~text
Git change
   |
   v
Argo CD detects OutOfSync
   |
   v
Notification
   |
   v
Operator reviews diff and health
   |
   v
Manual Sync
   |
   v
Production
~~~

## Image tag flow

Example fake image:

~~~text
registry.example.local/example/example-app:1.2.3
~~~

CI can update the GitOps manifest to the new tag. Argo CD then observes the Git revision and reconciles the stage application.

All names, registries, tags and addresses in this document are fake.

## Rollback

Prefer reverting the GitOps change or selecting an approved Git revision according to the release procedure. This keeps the desired state auditable.
