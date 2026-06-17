# User-Facing Applications

[<- Back to Kubernetes](../README.md)

This directory documents applications that run on the cluster and are used directly by people.

They are different from platform services. PostgreSQL, Traefik, Prometheus and Dapr help the cluster or applications operate. Nextcloud and Plex are end-user applications that consume the platform.

---

## Why This Matters

Applications are the reason the platform exists. They are what a user actually opens in a browser, mobile app or desktop client. Unlike infrastructure components, they are not required for Kubernetes to function, but they prove whether the platform is useful.

In a homelab, user-facing apps are practical tests. Nextcloud tests storage, ingress, TLS, database reliability and backups. Plex tests media storage, network access and hardware placement. These apps turn abstract infrastructure into workflows people care about.

In companies, the same distinction matters: platform services enable product applications, but they are not the product themselves. Keeping that boundary clear prevents every installed app from being treated like core infrastructure.

---

## What You Can Do With It

- run personal cloud applications
- test real stateful workloads
- expose apps through Traefik
- connect apps to Keycloak SSO
- validate backups with user data
- decide which apps deserve long-term operational support
- keep user-facing workloads separate from cluster-critical services

---

## Application Catalog

| Path | Status | Location | Recommendation | Purpose |
|---|---|---|---|---|
| [`./nextcloud`](./nextcloud) | ⚫ Inactive | Self-hosted app | Good user-facing homelab app | File sync, sharing and personal cloud features |
| [`./plex`](./plex) | ⚫ Inactive | Self-hosted app | Optional/lifestyle app | Media library and streaming server |

---

## Placement Rule

Put something here when all of these are true:

- it is installed into the cluster
- users interact with it directly
- it is not required for Kubernetes itself to function
- it consumes platform services instead of being one

Examples:

- Nextcloud
- Plex
- Home Assistant
- Immich
- Paperless-ngx

Do not put custom code here. Custom APIs, workers and operators written for this homelab belong in [`../../../services`](../../../services).

---

## Deployment Rule

Application documentation lives here. Helm charts, values and release definitions should live under:

```text
../../../../helm-charts/applications/<application-name>/
```
