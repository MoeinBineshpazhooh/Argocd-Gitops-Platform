# Production Approval Model

The demonstrated model separates validation from production rollout.

## Stage

~~~text
Git change
   |
   v
Argo CD
   |
   v
Stage
   |
   v
Healthy / validation
~~~

## Production

~~~text
Git change
   |
   v
Production Application
   |
   v
OutOfSync
   |
   v
Notification
   |
   v
Operator review
   |
   v
Manual Sync
~~~

Production is deliberately not configured for automated synchronization in the example. This allows a validated revision to be reviewed before production deployment.

## UI workflow

1. Open Applications.
2. Select the production application.
3. Confirm the Git revision.
4. Review the application diff.
5. Check resource health.
6. Start Sync after validation.
7. Monitor the resource tree and health.

## CLI equivalent

~~~bash
argocd app get example-app-production
argocd app diff example-app-production
argocd app sync example-app-production
~~~

All example names are fake.
