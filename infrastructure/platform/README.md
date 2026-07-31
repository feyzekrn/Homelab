# Platform Services

[<- Back to Infrastructure](../README.md)

This directory is the catalog of shared services that other workloads depend on: DNS, ingress, TLS, storage, databases, messaging, security, observability, backups, registries, runtimes and API tooling. Most run on the Kubernetes cluster; some deliberately live on the Proxmox host (`pve`) because they serve the stable world or the whole network — the `Runs on` column marks the placement per component.

The cluster itself — bootstrap, CNI, LoadBalancer IPs, GitOps, operators — is documented separately in [`kubernetes`](../kubernetes). User-facing apps such as Nextcloud or Jellyfin live in [`applications`](../../applications). Routing and firewalling at network level are not platform services either: the router lives with the network hardware it belongs to, in [`router`](../../setup/networking/router). This directory is the layer in between: not the engine, not the destination, but everything a real platform provides to its workloads.

A useful cluster is never just Kubernetes. Applications need names, routes, certificates, volumes, databases, queues, secrets, dashboards and restore paths. This directory is the map of those building blocks.

For beginners, read this catalog as a set of layers, not as an installation checklist. DNS and ingress are foundational. Kafka, service mesh and OpenSearch are advanced or workload-dependent. The right platform is the smallest one that teaches the target concepts and supports the real applications.

---

## How To Read This Catalog

Each component page explains the concept first and the project decision second. The docs intentionally include alternatives and weaknesses because a homelab should teach decision-making, not only tool names.

Every component row links to the locations that apply to it, following the [Component Layout Convention](../../README.md#component-layout-convention):

- `docs`: the local README explaining what the component is and why it exists here
- `chart`: the planned Helm chart location under [`helm-charts`](../../helm-charts), mirroring this tree — **only for `k8s` components**, since Proxmox guests are not deployed by Helm
- `config`: the optional Terraform directory next to the docs, for configuration IaC

Which links a row carries follows one rule:

| Row type | Links |
|---|---|
| Planned on the cluster | `docs` · `chart` · `config` |
| Planned as a Proxmox guest (`vm`/`lxc`) | `docs` · `config` |
| Documented alternative, not planned | `docs` only |

Chart and config directories are created when a component becomes active — most do not exist yet, by design.

Status meanings:

- `🟢 Active`: currently deployed or actively operated in the cluster
- `⚫ Inactive`: documented, planned or available for future use, but not currently running

Current state: every component is `⚫ Inactive` until the cluster build starts.

`Runs on` says **where a component is planned to run**:

| Value | Meaning |
|---|---|
| `k8s` | Workload on the bare-metal Kubernetes cluster |
| `k8s ⚓` | On the cluster, but with one replica **pinned to the Proxmox-hosted node** so it survives a cluster rebuild |
| `lxc` | Container on the Proxmox host — the default for lightweight services in the stable world |
| `vm` | Full virtual machine on the Proxmox host — when a component brings its own operating system |
| `lxc + k8s` | Instances in both worlds (AdGuard Home: primary plus synced replica; Cloudflare Tunnel: one connector per world) |
| `—` | Documented alternative or category — nothing to deploy |

The split is not about capability but about **blast radius**: anything the household depends on runs where cluster experiments cannot reach it, and anything that benefits from rescheduling across nodes runs on the cluster.

The rule that decides a placement is *who consumes the component*, not how much availability it needs — documented in full under [The Bridge](../../setup/compute/README.md#the-bridge-one-node-with-a-foot-in-both-worlds). Components whose consumers live in both worlds get the `⚓` anchor; components the cluster alone consumes stay plain `k8s` even when they are important, because their usefulness ends when the cluster does.

`Idle RAM` is a rough ballpark per instance at homelab scale — what the component consumes just by running, before real load. Values marked `/ node` run on every node (DaemonSet-style), `each`/`sidecar` multiply per use. Load, caches and data change the picture; treat the column as an order-of-magnitude guide, not a promise.

Two takeaways from the column: the chosen access stack (Traefik + CoreDNS + AdGuard + Cloudflare Tunnel + NetBird peer + Caddy) sums to **under 0.5 GB** across both worlds — the glue is cheap. The expensive components are the JVM- and search-shaped ones (Keycloak, Harbor, Nexus) and the ML-heavy apps; those are exactly the ones planned for later or left as documented alternatives.

Recommendation meanings:

- `Unavoidable`: needed for this platform to make sense
- `Standard`: a common default for this layer
- `Recommended`: good first choice for this homelab
- `Optional`: useful only when a workload needs it
- `Advanced/later`: interesting, but not an early dependency

---

## Directory Layout

```text
infrastructure/platform/
├── api/
│   └── graphql/
├── backup/
│   ├── proxmox-backup-server/
│   └── velero/
├── databases/
│   ├── influxdb/
│   ├── mongodb/
│   ├── mysql/
│   ├── postgresql/
│   └── redis/
├── dns/
│   ├── adguard-home/
│   ├── coredns/
│   ├── duckdns/
│   └── pihole/
├── ingress/
│   ├── caddy/
│   ├── cert-manager/
│   ├── cloudflare-tunnel/
│   ├── netbird/
│   └── traefik/
├── messaging/
│   ├── kafka/
│   ├── nats/
│   └── rabbitmq/
├── observability/
│   ├── logging/
│   │   ├── fluent-bit/
│   │   ├── loki/
│   │   └── opensearch/
│   ├── metrics/
│   │   ├── grafana/
│   │   └── prometheus/
│   └── tracing/
│       ├── jaeger/
│       ├── opentelemetry-collector/
│       └── zipkin/
├── registry/
│   ├── artifact-repository/
│   ├── forgejo/
│   ├── github-packages/
│   └── harbor/
├── runtime/
│   ├── dapr/
│   └── service-mesh/
├── security/
│   ├── external-secrets/
│   ├── openbao/
│   ├── password-manager/
│   │   └── bitwarden/
│   ├── rights-management/
│   │   └── keycloak/
│   ├── sealed-secrets/
│   └── secret-store/
└── storage/
    ├── longhorn/
    ├── minio/
    ├── openmediavault/
    ├── truenas/
    └── zfs-nas/
```

---

## Service Catalog

### DNS

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| CoreDNS | [docs](./dns/coredns) · [chart](../../helm-charts/infrastructure/platform/dns/coredns) · [config](./dns/coredns/terraform) | ⚫ Inactive | k8s | ~30–50 MB | Cluster DNS and authoritative internal zone DNS | Chosen: cluster and internal DNS | 2026-07-11 |
| AdGuard Home | [docs](./dns/adguard-home) · [chart](../../helm-charts/infrastructure/platform/dns/adguard-home) · [config](./dns/adguard-home/terraform) | ⚫ Inactive | lxc + k8s | ~50–100 MB | LAN resolver with network-wide ad/tracker blocking | Chosen LAN resolver: primary LXC, synced replica on the cluster | 2026-07-28 |
| Pi-hole | [docs](./dns/pihole) | ⚫ Inactive | — | ~50–100 MB | Classic filtering DNS resolver | Documented alternative to AdGuard Home | 2026-07-08 |
| DuckDNS | [docs](./dns/duckdns) | ⚫ Inactive | — | ≈ 0 (CronJob) | Free dynamic DNS for a changing home IP | Dropped: an own domain plus Cloudflare Tunnel removes the need | 2026-07-28 |

### Ingress And External Access

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| Traefik | [docs](./ingress/traefik) · [chart](../../helm-charts/infrastructure/platform/ingress/traefik) · [config](./ingress/traefik/terraform) | ⚫ Inactive | k8s | ~100–150 MB | Reverse proxy that exposes HTTP(S) services | Chosen ingress controller | 2026-07-11 |
| cert-manager | [docs](./ingress/cert-manager) · [chart](../../helm-charts/infrastructure/platform/ingress/cert-manager) · [config](./ingress/cert-manager/terraform) | ⚫ Inactive | k8s | ~50–100 MB | Automatic TLS certificate management | Strongly recommended | 2026-06-17 |
| Cloudflare Tunnel | [docs](./ingress/cloudflare-tunnel) · [chart](../../helm-charts/infrastructure/platform/ingress/cloudflare-tunnel) · [config](./ingress/cloudflare-tunnel/terraform) | ⚫ Inactive | lxc + k8s | ~20–50 MB | External access to selected apps without VPN or port forwarding | Chosen for public app exposure: one connector per world | 2026-07-28 |
| NetBird | [docs](./ingress/netbird) · [config](./ingress/netbird/terraform) | ⚫ Inactive | lxc | ~50 MB peer | WireGuard mesh VPN with built-in reverse proxy for public exposure | Chosen for private/admin access — managed control plane, self-hosting later | 2026-07-28 |
| Caddy | [docs](./ingress/caddy) · [config](./ingress/caddy/terraform) | ⚫ Inactive | lxc | ~30–50 MB | Reverse proxy with automatic HTTPS by default | Chosen reverse proxy for the Proxmox world; Traefik stays cluster-only | 2026-07-28 |

### Security

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| Secret Store (Vault) | [docs](./security/secret-store) · [chart](../../helm-charts/infrastructure/platform/security/secret-store) · [config](./security/secret-store/terraform) | ⚫ Inactive | k8s | ~0.2–0.5 GB | Central vault for app secrets, tokens and accounts | Chosen: HashiCorp Vault, the industry standard | 2026-07-28 |
| OpenBao | [docs](./security/openbao) | ⚫ Inactive | — | ~0.2–0.5 GB | Open-source fork of Vault under the Linux Foundation, API-compatible | Documented alternative — the drop-in if Vault's licence becomes a problem | 2026-07-28 |
| External Secrets Operator | [docs](./security/external-secrets) · [chart](../../helm-charts/infrastructure/platform/security/external-secrets) · [config](./security/external-secrets/terraform) | ⚫ Inactive | k8s | ~50–100 MB | Syncs selected vault secrets into Kubernetes Secrets | GitOps standard | 2026-06-17 |
| Sealed Secrets | [docs](./security/sealed-secrets) | ⚫ Inactive | — | ~50 MB | Encrypted Kubernetes Secrets stored in Git | Documented alternative — not needed alongside Vault | 2026-07-28 |
| Rights Management | [docs](./security/rights-management) | ⚫ Inactive | — | — | Identity, roles and app permission decisions (category) | Important later | 2026-06-17 |
| Keycloak | [docs](./security/rights-management/keycloak) · [chart](../../helm-charts/infrastructure/platform/security/rights-management/keycloak) · [config](./security/rights-management/keycloak/terraform) | ⚫ Inactive | k8s ⚓ | ~0.7–1 GB | Identity provider for SSO, OIDC, OAuth2, users, groups and service accounts | Chosen identity provider — anchored, database on `pve0` | 2026-07-30 |
| PostgreSQL (identity) | [docs](./databases/postgresql) · [config](./databases/postgresql/terraform) | ⚫ Inactive | lxc | ~0.1–0.3 GB | Dedicated database for Keycloak, kept outside the cluster | Required by the anchor — a pinned pod with a cluster-side database anchors nothing | 2026-07-30 |
| Password Manager | [docs](./security/password-manager) | ⚫ Inactive | — | — | Human password vault, separate from application secrets (category) | High daily value | 2026-07-08 |
| Bitwarden (Vaultwarden) | [docs](./security/password-manager/bitwarden) · [config](./security/password-manager/bitwarden/terraform) | ⚫ Inactive | lxc | ~50–100 MB | Family password manager (Vaultwarden server, Bitwarden clients) | Chosen password manager | 2026-07-28 |

### Storage

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| Longhorn | [docs](./storage/longhorn) · [chart](../../helm-charts/infrastructure/platform/storage/longhorn) · [config](./storage/longhorn/terraform) | ⚫ Inactive | k8s | ~0.3–0.5 GB / node | Persistent volumes for stateful Kubernetes workloads | Storage standard for the cluster | 2026-06-17 |
| ZFS + shares 🗄️ NAS | [docs](./storage/zfs-nas) · [config](./storage/zfs-nas/terraform) | ⚫ Inactive | lxc | ~0.1 GB service + ZFS ARC | ZFS pool on the Proxmox host, exported through a small share container | Chosen NAS approach | 2026-07-28 |
| TrueNAS SCALE 🗄️ NAS | [docs](./storage/truenas) | ⚫ Inactive | — | ~8–16 GB | Full NAS operating system with a web UI, run as a VM | Documented alternative — costs the bind-mount architecture | 2026-07-28 |
| OpenMediaVault 🗄️ NAS | [docs](./storage/openmediavault) | ⚫ Inactive | — | ~1–2 GB | Debian-based NAS distribution, lighter than TrueNAS | Documented alternative | 2026-07-28 |
| MinIO (apps) | [docs](./storage/minio) · [chart](../../helm-charts/infrastructure/platform/storage/minio) · [config](./storage/minio/terraform) | ⚫ Inactive | k8s | ~0.2–0.5 GB | S3 endpoint for application buckets — uploads, images, exports | Chosen object storage for apps — single replica on Longhorn | 2026-07-30 |
| MinIO (backup) | [docs](./storage/minio) · [config](./storage/minio/terraform) | ⚫ Inactive | lxc | ~0.2–0.5 GB | S3 backup target on `tank/backups` | Chosen backup target — must outlive the cluster | 2026-07-30 |

### Databases And Data Stores

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| PostgreSQL | [docs](./databases/postgresql) · [chart](../../helm-charts/infrastructure/platform/databases/postgresql) · [config](./databases/postgresql/terraform) | ⚫ Inactive | k8s | ~0.1–0.3 GB | Main SQL database for custom services and cluster workloads | Chosen default database | 2026-07-30 |
| Redis | [docs](./databases/redis) · [chart](../../helm-charts/infrastructure/platform/databases/redis) · [config](./databases/redis/terraform) | ⚫ Inactive | k8s | ~30–100 MB | Fast cache, session store and lightweight key-value system | Chosen cache — deployed once an app needs it | 2026-07-28 |
| MySQL | [docs](./databases/mysql) | ⚫ Inactive | — | ~0.3–0.5 GB | SQL database for MySQL-compatible apps and learning | Documented alternative to PostgreSQL | 2026-07-28 |
| MongoDB | [docs](./databases/mongodb) | ⚫ Inactive | — | ~0.3–1 GB | Document database for JSON-shaped data | Documented — deploy only for a real workload | 2026-07-28 |
| InfluxDB | [docs](./databases/influxdb) | ⚫ Inactive | — | ~0.2–0.5 GB | Time-series database for sensors and measurements | Documented — Prometheus covers metrics for now | 2026-07-28 |

**PostgreSQL runs more than once, on purpose.** The cluster instance above serves cluster workloads. A second, separate instance runs as an `lxc` on `pve0` for [Keycloak](./security/rights-management/keycloak#where-it-runs--the-hardest-placement-in-the-catalog) — see the identity row in the Security section. And the family apps on `pve0` keep their databases inside their own containers rather than sharing one, so that each app is a single self-contained `vzdump` and no shared database outage can take all three offline at once. One database engine, four deployments, three different reasons.

### Messaging

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| NATS | [docs](./messaging/nats) · [chart](../../helm-charts/infrastructure/platform/messaging/nats) · [config](./messaging/nats/terraform) | ⚫ Inactive | k8s | ~20–50 MB | Lightweight event bus for simple service communication | Chosen event bus — also the MQTT broker for IoT | 2026-07-28 |
| RabbitMQ | [docs](./messaging/rabbitmq) | ⚫ Inactive | — | ~0.15–0.3 GB | Message broker for queues, retries and workers | Documented — revisit when real job queues appear | 2026-07-28 |
| Kafka | [docs](./messaging/kafka) | ⚫ Inactive | — | ~1–2 GB+ | Durable event log for replayable streams | Documented alternative — too heavy for this scale | 2026-07-28 |

### API Platform

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| GraphQL | [docs](./api/graphql) | ⚫ Inactive | — | ~0.1–0.3 GB | API layer that combines data for clients and dashboards | Documented — decided per custom service, not as platform infrastructure | 2026-07-28 |

### Observability

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| Prometheus | [docs](./observability/metrics/prometheus) · [chart](../../helm-charts/infrastructure/platform/observability/metrics/prometheus) · [config](./observability/metrics/prometheus/terraform) | ⚫ Inactive | k8s | ~0.5–1 GB+ | Metrics database and alerting engine | Chosen metrics stack — also scrapes `pve0` and the switch | 2026-07-28 |
| Grafana | [docs](./observability/metrics/grafana) · [chart](../../helm-charts/infrastructure/platform/observability/metrics/grafana) · [config](./observability/metrics/grafana/terraform) | ⚫ Inactive | k8s | ~0.15–0.3 GB | Dashboard UI for metrics, logs and traces | Chosen dashboard layer | 2026-07-28 |
| Loki | [docs](./observability/logging/loki) · [chart](../../helm-charts/infrastructure/platform/observability/logging/loki) · [config](./observability/logging/loki/terraform) | ⚫ Inactive | k8s | ~0.2–0.4 GB | Log backend that indexes labels instead of full text | Chosen logging backend — shares Grafana with the metrics | 2026-07-30 |
| Fluent Bit | [docs](./observability/logging/fluent-bit) · [chart](../../helm-charts/infrastructure/platform/observability/logging/fluent-bit) · [config](./observability/logging/fluent-bit/terraform) | ⚫ Inactive | k8s | ~30–50 MB / node | Lightweight log collector for Kubernetes nodes | Chosen log collector — ships into Loki | 2026-07-30 |
| OpenTelemetry Collector | [docs](./observability/tracing/opentelemetry-collector) · [chart](../../helm-charts/infrastructure/platform/observability/tracing/opentelemetry-collector) · [config](./observability/tracing/opentelemetry-collector/terraform) | ⚫ Inactive | k8s | ~0.1–0.2 GB | Neutral pipeline for traces, metrics and logs | Chosen — deployed once custom services exist | 2026-07-28 |
| Jaeger | [docs](./observability/tracing/jaeger) · [chart](../../helm-charts/infrastructure/platform/observability/tracing/jaeger) · [config](./observability/tracing/jaeger/terraform) | ⚫ Inactive | k8s | ~0.2–0.5 GB | Trace UI/backend for distributed services | Chosen tracing backend — same timing as the collector | 2026-07-28 |
| OpenSearch | [docs](./observability/logging/opensearch) | ⚫ Inactive | — | ~2–4 GB+ | Search engine for logs and analytics | Documented alternative — too heavy; Loki is the lighter path | 2026-07-28 |
| Zipkin | [docs](./observability/tracing/zipkin) | ⚫ Inactive | — | ~0.3–0.5 GB | Simpler tracing backend and compatibility target | Documented alternative to Jaeger | 2026-07-28 |

### Backup

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| Velero | [docs](./backup/velero) · [chart](../../helm-charts/infrastructure/platform/backup/velero) · [config](./backup/velero/terraform) | ⚫ Inactive | k8s | ~0.1–0.2 GB | Backup and restore tool for Kubernetes resources and volumes | Chosen for the cluster — targets MinIO | 2026-07-28 |
| Proxmox Backup Server | [docs](./backup/proxmox-backup-server) · [config](./backup/proxmox-backup-server/terraform) | ⚫ Inactive | vm | ~1–2 GB | Deduplicating backup server for Proxmox VMs and containers | Planned later — `vzdump` to the ZFS pool covers the start | 2026-07-28 |

### Registry

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| Harbor | [docs](./registry/harbor) · [chart](../../helm-charts/infrastructure/platform/registry/harbor) · [config](./registry/harbor/terraform) | ⚫ Inactive | k8s | ~1–2 GB | Private container registry for images, Helm charts and OCI artifacts | Chosen registry — first component after the cluster runs | 2026-07-28 |
| Artifact Repository (Nexus) | [docs](./registry/artifact-repository) · [chart](../../helm-charts/infrastructure/platform/registry/artifact-repository) · [config](./registry/artifact-repository/terraform) | ⚫ Inactive | k8s | ~1.5–2.5 GB | Private package registry for npm, NuGet, Maven and generic artifacts | Planned later — Harbor cannot serve npm | 2026-07-28 |
| GitHub Packages | [docs](./registry/github-packages) | ⚫ Inactive | — | — (external) | Hosted package registry attached to the GitHub repositories | Not planned — the free bridge for private npm until Nexus exists | 2026-07-28 |
| Forgejo / Gitea | [docs](./registry/forgejo) | ⚫ Inactive | — | ~0.3 GB | Self-hosted Git server with a built-in multi-format package registry | Documented alternative — CI and repos deliberately stay on GitHub | 2026-07-28 |

### Runtime

| Name | Path | Status | Runs on | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|---|
| Dapr | [docs](./runtime/dapr) | ⚫ Inactive | — | ~0.3 GB + ~50 MB sidecar / app | App runtime for pub/sub, state, secrets and service calls | Documented — revisit once several custom services exist | 2026-07-28 |
| Service Mesh | [docs](./runtime/service-mesh) | ⚫ Inactive | — | ~0.5–1 GB + sidecars | Traffic security and control between services | Documented — Cilium already covers much of this | 2026-07-28 |

---

## Recommended Baseline

For the first serious build, keep the always-running baseline small — and note that it now spans both worlds:

**On the Proxmox host, first:** the ZFS pool with its datasets, AdGuard Home as the primary resolver, Caddy in front of the family apps, and NetBird for access from outside. This half is what the household actually notices, and it works before a single Kubernetes node exists.

**On the cluster, once it runs:** Traefik and cert-manager for the first exposed service, CoreDNS for internal names, Longhorn for block storage, PostgreSQL as the primary database with Redis when an app needs caching, Prometheus and Grafana once there is something to observe, and Velero before any data becomes irreplaceable.

Everything else can be added when there is a real workload or learning goal. This keeps the platform understandable and avoids turning the first build into a permanent maintenance queue.

---

## Deployment Rule

This directory answers:

- What is the component?
- Why does this project care?
- Should it run all the time?
- What are the main alternatives?
- What should be monitored?

Deployment assets follow the repository convention (see the [root README](../../README.md#component-layout-convention)):

```text
../../helm-charts/infrastructure/platform/<category>/<component>/    # chart — Helm chart, mirrors this tree
./<category>/<component>/terraform/                # config — optional Terraform for configuration
```

---

## Learning Links

- [Wikipedia: Kubernetes](https://en.wikipedia.org/wiki/Kubernetes)
- [Kubernetes concepts documentation](https://kubernetes.io/docs/concepts/)
- [Wikipedia: Platform engineering](https://en.wikipedia.org/wiki/Platform_engineering)
- [Wikipedia: Microservices](https://en.wikipedia.org/wiki/Microservices)
