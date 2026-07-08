# User-Facing Applications

[<- Back to Repository Overview](../README.md)

This directory documents applications that run on the cluster and are used directly by people.

They are different from platform services. PostgreSQL, Traefik, Prometheus and Dapr help the cluster or applications operate. Nextcloud, Immich and Jellyfin are end-user applications that consume the platform.

User-facing applications are the things a person opens in a browser, mobile app or desktop client. They are the visible reason the platform exists.

Platform services usually support other workloads. A database stores data. An ingress controller routes traffic. A storage system provides persistent volumes. A user-facing application consumes those services to provide an actual experience, such as file sync, media streaming or document management.

This separation matters because not every installed application should become core infrastructure. If Jellyfin is down, media streaming is affected. If Cilium, storage or DNS is down, the platform itself is affected.

---

## Why This Matters

Applications are the reason the platform exists. They are what a user actually opens in a browser, mobile app or desktop client. Unlike infrastructure components, they are not required for Kubernetes to function, but they prove whether the platform is useful.

In a homelab, user-facing apps are practical tests. Nextcloud tests storage, ingress, TLS, database reliability and backups. Jellyfin tests media storage, network access and hardware placement. Immich tests multi-service deployments and real data growth. These apps turn abstract infrastructure into workflows people care about.

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

Each row links up to three locations, following the [Component Layout Convention](../README.md#component-layout-convention): `docs` (local README), `chart` (planned Helm chart under [`../helm-charts`](../helm-charts)) and `config` (optional Terraform next to the docs). Chart and config directories are created when an application becomes active; documented alternatives get docs only.

| Name | Path | Status | Recommendation | Purpose |
|---|---|---|---|---|
| Nextcloud | [docs](./nextcloud) · [chart](../helm-charts/applications/nextcloud) · [config](./nextcloud/terraform) | ⚫ Inactive | Chosen personal cloud | Files, calendars and contacts as the family's source of truth |
| ownCloud | [docs](./owncloud) | ⚫ Inactive | Documented alternative to Nextcloud | Lean file sync platform (oCIS); not planned for deployment |
| Immich | [docs](./immich) · [chart](../helm-charts/applications/immich) · [config](./immich/terraform) | ⚫ Inactive | Chosen photo platform | Family photo cloud replacing iCloud/Google Photos |
| Jellyfin | [docs](./jellyfin) · [chart](../helm-charts/applications/jellyfin) · [config](./jellyfin/terraform) | ⚫ Inactive | Chosen media server | Fully open-source media library and streaming |
| Plex | [docs](./plex) | ⚫ Inactive | Documented alternative to Jellyfin | Polished media server; not planned for deployment |

---

## Placement Rule

Put something here when all of these are true:

- it is installed into the cluster
- users interact with it directly
- it is not required for Kubernetes itself to function
- it consumes platform services instead of being one

Examples:

- Nextcloud
- Immich
- Jellyfin
- Home Assistant
- Paperless-ngx

Do not put custom code here. Custom APIs, workers and operators written for this homelab belong in [`../services`](../services).

---

## Operational Questions

Every user-facing application should answer:

- What data does it store?
- Which database does it need?
- Which volumes or buckets does it use?
- How is it exposed through ingress?
- Does it support SSO?
- How is it backed up and restored?
- Is it important enough to run permanently?

---

## Deployment Rule

Application documentation lives here. Helm charts, values and release definitions should live under:

```text
../helm-charts/applications/<application-name>/
```

---

## Learning Links

- [Wikipedia: Self-hosting](https://en.wikipedia.org/wiki/Self-hosting_(web_services))
- [Wikipedia: Web application](https://en.wikipedia.org/wiki/Web_application)
- [Kubernetes workloads documentation](https://kubernetes.io/docs/concepts/workloads/)
