# Argo CD Notifications

Argo CD Notifications can send application-state alerts to external communication channels. This document describes available configuration options; it does not claim that every option is deployed in the environment.

The environment includes the Argo CD Notifications Controller and uses it to alert operators when an application requires attention.

## Controller

~~~bash
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-notifications-controller
~~~

## Notification options

### Email

Email can be used for operational alerts such as OutOfSync, sync failures and health degradation.

Fake recipient:

~~~text
platform-alerts@example.local
~~~

### Slack

Slack can be used for team/channel-based operational alerts.

Fake channel:

~~~text
#example-argocd-alerts
~~~

A real Slack token or webhook must be stored securely and never committed to Git.

### Telegram Bot

Telegram can be used through a Telegram Bot for fast mobile/team-chat notifications.

Fake bot:

~~~text
@example_argocd_alert_bot
~~~

Fake bot token:

~~~text
123456789:FAKE-TELEGRAM-BOT-TOKEN-ONLY
~~~

A real Telegram bot token must never be committed to Git.

## Notification architecture

~~~text
                    Argo CD
                       |
                       v
          Notifications Controller
                       |
          +------------+-------------+
          |            |             |
          v            v             v
        Email        Slack       Telegram
                                   Bot
~~~

These are alternative notification destinations. They do not need to be enabled simultaneously.

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


## Portfolio scope

This section documents **available notification integration patterns and configuration options**. It should not be interpreted as claiming that Email, Slack and Telegram were all deployed or simultaneously configured in the production environment.
