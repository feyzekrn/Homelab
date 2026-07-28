# User-Facing Applications

[<- Back to Repository Overview](../README.md)

This directory documents applications that run in the homelab and are used directly by people — some on the Kubernetes cluster, some as guests on the Proxmox host. Where an app runs follows the availability rule: family-facing, stable apps live on `pve` (LXCs on the MS-01), experimental and HA-dependent apps live on `k8s`.

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
- expose apps through Traefik (k8s) or Caddy (pve)
- connect apps to Keycloak SSO
- validate backups with user data
- decide which apps deserve long-term operational support
- keep user-facing workloads separate from cluster-critical services

---

## Application Catalog

Each row links up to three locations, following the [Component Layout Convention](../README.md#component-layout-convention): `docs` (local README), `chart` (planned Helm chart under [`helm-charts`](../helm-charts)) and `config` (optional Terraform next to the docs). Chart and config directories are created when an application becomes active; documented alternatives get docs only.

`Idle RAM` is a rough ballpark for the app itself — databases, caches and storage it depends on are counted in the [platform catalog](../infrastructure/platform/README.md). Note that the apps, not the infrastructure glue, are where the real memory goes: Immich's machine learning alone outweighs the entire ingress and DNS stack many times over.

`Runs on` marks the target world: `k8s` (bare-metal cluster) or `pve` (LXC/VM on the Proxmox host) — see the [compute overview](../setup/compute) for the reasoning behind the split.

| Name | Path | Status | Runs on | Idle RAM | Recommendation | Purpose |
|---|---|---|---|---|---|---|
| Home Assistant | [docs](./home-assistant) · [chart](../helm-charts/applications/home-assistant) · [config](./home-assistant/terraform) | ⚫ Inactive | k8s | ~0.5–1 GB | Chosen automation platform | Local-first home automation, the flagship cluster app |
| Immich | [docs](./immich) · [config](./immich/terraform) | ⚫ Inactive | lxc | ~2–4 GB | Chosen photo platform | Family photo cloud replacing iCloud/Google Photos |
| Jellyfin | [docs](./jellyfin) · [config](./jellyfin/terraform) | ⚫ Inactive | lxc | ~0.5–1 GB | Chosen media server | Fully open-source media library and streaming |
| Nextcloud | [docs](./nextcloud) · [config](./nextcloud/terraform) | ⚫ Inactive | lxc | ~0.5–1 GB | Chosen personal cloud | Files, calendars and contacts as the family's source of truth |
| ownCloud | [docs](./owncloud) | ⚫ Inactive | — | ~0.2 GB (oCIS) | Documented alternative to Nextcloud | Lean file sync platform (oCIS); not planned for deployment |
| Plex | [docs](./plex) | ⚫ Inactive | — | ~0.5–1 GB | Documented alternative to Jellyfin | Polished media server; not planned for deployment |

**Why the split falls this way.** The three media and file apps land in containers on the Proxmox host: they hold family data, they must survive cluster experiments, and they read their datasets as local bind-mounts from the ZFS pool — no network storage path involved, and no dependency on the cluster being healthy. Home Assistant is the deliberate exception: it controls physical devices, an outage is felt immediately, and its state is small enough to move — which is exactly what multi-node failover is for.

---

## Placement Rule

Put something here when all of these are true:

- it runs in the homelab (on the cluster or as a Proxmox guest)
- users interact with it directly
- it is not required for the platform itself to function
- it consumes platform services instead of being one

Examples: Nextcloud, Immich, Jellyfin, Home Assistant, Paperless-ngx.

Do not put custom code here. Custom APIs, workers and operators written for this homelab belong in [`services`](../services).

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

Application documentation lives here. For `k8s`-hosted apps, Helm charts, values and release definitions live under:

```text
../helm-charts/applications/<application-name>/
```

For `pve`-hosted apps, the guest definitions (LXC/VM configuration as code) will live under the planned `infrastructure/proxmox` section — the docs here stay the single source for the what and why either way.

---

## Learning Links

- [Wikipedia: Self-hosting](https://en.wikipedia.org/wiki/Self-hosting_(web_services))
- [Wikipedia: Web application](https://en.wikipedia.org/wiki/Web_application)
- [Kubernetes workloads documentation](https://kubernetes.io/docs/concepts/workloads/)
