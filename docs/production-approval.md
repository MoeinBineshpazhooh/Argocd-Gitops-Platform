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

Both Applications track the moving `devops` branch. Disabling automated sync does not freeze that branch or enforce an approval policy. If another commit arrives during review, a plain Sync can deploy a newer, unvalidated revision. Approve an exact Git commit SHA and the immutable image tag/digest tested in stage. Restrict production sync privileges through your platform's RBAC process.

Stage health alone is not release approval. Record successful smoke/integration tests and verify that the production manifests at the approved commit use the same tested image artifacts; the two environment directories can differ.

## UI workflow

1. Open Applications.
2. Select the production application.
3. Confirm the exact commit SHA that passed stage tests.
4. Review the application diff.
5. Check resource health.
6. Select that exact SHA in the Sync revision field and start Sync after approval.
7. Monitor the resource tree and health.

## CLI procedure for these single-source examples

First inspect stage and confirm its deployed revision, synchronization and health. Record that SHA with the test results and image artifacts:

~~~bash
argocd app get example-app-stage --refresh
~~~

Set the full approved SHA explicitly. Do not resolve the current branch head at deployment time:

~~~bash
APPROVED_REVISION='<FULL_GIT_COMMIT_SHA_VALIDATED_IN_STAGE>'
argocd app get example-app-production --refresh
argocd app diff example-app-production --revision "$APPROVED_REVISION"
~~~

Review the diff and approve it before running the following commands. `app diff` returns a nonzero exit code when differences exist by default; distinguish an expected diff from an error. Do not add `--prune` without reviewing deletions.

~~~bash
argocd app sync example-app-production --revision "$APPROVED_REVISION"
argocd app wait example-app-production --operation --health --timeout 300
argocd app get example-app-production
~~~

Confirm the completed operation succeeded and deployed the approved SHA, then run production smoke tests. Because `targetRevision` still tracks `devops`, production may remain OutOfSync if the branch has advanced. Do not sync again merely to clear that status. `--revision` selects this operation's revision; it does not pin the Application's desired revision.

For a persistent desired-state release boundary, consider a separate production promotion change that updates a pinned commit or immutable release reference. That is an optional extension; these examples retain your manual production sync model.

## Rollback

Review and revert the release change in Git, validate the resulting manifests and image references, then follow the same approval and synchronization procedure. Account for database migrations and other changes that a manifest revert cannot undo.

## References

- [Argo CD app sync](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_sync/)
- [Argo CD app diff](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_diff/)

All example names are fake.
