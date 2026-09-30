# Argo CD Notifications

The environment includes the Argo CD Notifications Controller and uses it to alert operators when an application requires attention.

## Controller

~~~bash
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-notifications-controller
~~~

## Example alert

~~~text
Production Application
        |
        v
   OutOfSync detected
        |
        v
Notifications Controller
        |
        v
       SMTP
        |
        v
platform-alerts@example.local
~~~

All addresses and credentials in this repository are fake.

## Configuration

The example ConfigMap is:

~~~text
manifests/argocd/notifications-cm.yaml
~~~

The example Secret is:

~~~text
manifests/argocd/notifications-secret.example.yaml
~~~

The Secret is documentation only. Never replace its fake values with production credentials and commit it.

## Trigger

The example trigger sends an email when the production application's sync status becomes OutOfSync.

## Verification

~~~bash
kubectl get configmap argocd-notifications-cm -n argocd
kubectl get secret argocd-notifications-secret -n argocd
kubectl get pods -n argocd
kubectl logs -n argocd deploy/argocd-notifications-controller
~~~

Do not put credentials into Git, screenshots or portfolio documentation.

## Other protocols

Depending on the installed Argo CD Notifications version and configured services, notifications can be integrated with providers such as email, Slack, Microsoft Teams and webhooks. Select the provider supported by the target environment.
