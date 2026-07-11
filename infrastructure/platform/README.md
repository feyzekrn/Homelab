# Platform Services

[<- Back to Infrastructure](../README.md)

This directory is the catalog of shared services that run **on** the Kubernetes cluster and that other workloads depend on: DNS, ingress, TLS, storage, databases, messaging, security, observability, backups, registries, runtimes and API tooling.

The cluster itself — bootstrap, CNI, LoadBalancer IPs, GitOps, operators — is documented separately in [`../kubernetes`](../kubernetes). User-facing apps such as Nextcloud or Jellyfin live in [`../../applications`](../../applications). This directory is the layer in between: not the engine, not the destination, but everything a real platform provides to its workloads.

A useful cluster is never just Kubernetes. Applications need names, routes, certificates, volumes, databases, queues, secrets, dashboards and restore paths. This directory is the map of those building blocks.

For beginners, read this catalog as a set of layers, not as an installation checklist. DNS and ingress are foundational. Kafka, service mesh and OpenSearch are advanced or workload-dependent. The right platform is the smallest one that teaches the target concepts and supports the real applications.

---

## How To Read This Catalog

Each component page explains the concept first and the project decision second. The docs intentionally include alternatives and weaknesses because a homelab should teach decision-making, not only tool names.

Every component row links up to three locations, following the [Component Layout Convention](../../README.md#component-layout-convention):

- `docs`: the local README explaining what the component is and why it exists here
- `chart`: the planned Helm chart location under [`../../helm-charts`](../../helm-charts), mirroring this tree
- `config`: the optional Terraform directory next to the docs, for configuration IaC

Chart and config directories are created when a component becomes active — most do not exist yet, by design.

Status meanings:

- `🟢 Active`: currently deployed or actively operated in the cluster
- `⚫ Inactive`: documented, planned or available for future use, but not currently running

Current state: every component is `⚫ Inactive` until the cluster build starts.

`Idle RAM` is a rough ballpark per instance at homelab scale — what the component consumes just by running, before real load. Values marked `/ node` run on every node (DaemonSet-style), `each`/`sidecar` multiply per use. Load, caches and data change the picture; treat the column as an order-of-magnitude guide, not a promise.

Two takeaways from the column: the chosen access stack (Traefik + CoreDNS + AdGuard + Cloudflare Tunnel + NetBird peer + DuckDNS) sums to **under 0.5 GB** across the whole cluster — the glue is cheap. The expensive components are the JVM- and search-shaped ones (Keycloak, Kafka, OpenSearch, Nexus/Harbor) and the ML-heavy apps; those are exactly the ones marked `Optional` or `Advanced/later`.

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
│   └── harbor/
├── runtime/
│   ├── dapr/
│   └── service-mesh/
├── security/
│   ├── external-secrets/
│   ├── password-manager/
│   │   └── bitwarden/
│   ├── rights-management/
│   │   └── keycloak/
│   ├── sealed-secrets/
│   └── secret-store/
└── storage/
    ├── longhorn/
    └── minio/
```

---

## Service Catalog

### DNS

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| CoreDNS | [docs](./dns/coredns) · [chart](../../helm-charts/infrastructure/platform/dns/coredns) · [config](./dns/coredns/terraform) | ⚫ Inactive | ~30–50 MB | Cluster DNS and authoritative internal zone DNS | Chosen: cluster and internal DNS | 2026-07-11 |
| AdGuard Home | [docs](./dns/adguard-home) · [chart](../../helm-charts/infrastructure/platform/dns/adguard-home) · [config](./dns/adguard-home/terraform) | ⚫ Inactive | ~50–100 MB | LAN resolver with network-wide ad/tracker blocking | Chosen LAN resolver | 2026-07-08 |
| Pi-hole | [docs](./dns/pihole) | ⚫ Inactive | ~50–100 MB | Classic filtering DNS resolver | Documented alternative to AdGuard Home | 2026-07-08 |
| DuckDNS | [docs](./dns/duckdns) · [chart](../../helm-charts/infrastructure/platform/dns/duckdns) · [config](./dns/duckdns/terraform) | ⚫ Inactive | ≈ 0 (CronJob) | Free dynamic DNS for a changing home IP | Chosen: free public name for entry points | 2026-07-11 |

### Ingress And External Access

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| Traefik | [docs](./ingress/traefik) · [chart](../../helm-charts/infrastructure/platform/ingress/traefik) · [config](./ingress/traefik/terraform) | ⚫ Inactive | ~100–150 MB | Reverse proxy that exposes HTTP(S) services | Chosen ingress controller | 2026-07-11 |
| cert-manager | [docs](./ingress/cert-manager) · [chart](../../helm-charts/infrastructure/platform/ingress/cert-manager) · [config](./ingress/cert-manager/terraform) | ⚫ Inactive | ~50–100 MB | Automatic TLS certificate management | Strongly recommended | 2026-06-17 |
| Cloudflare Tunnel | [docs](./ingress/cloudflare-tunnel) · [chart](../../helm-charts/infrastructure/platform/ingress/cloudflare-tunnel) · [config](./ingress/cloudflare-tunnel/terraform) | ⚫ Inactive | ~20–50 MB | External access to selected apps without VPN or port forwarding | Chosen for public app exposure | 2026-07-11 |
| NetBird | [docs](./ingress/netbird) · [chart](../../helm-charts/infrastructure/platform/ingress/netbird) · [config](./ingress/netbird/terraform) | ⚫ Inactive | ~50 MB peer / ~0.5 GB self-hosted stack | WireGuard mesh VPN with built-in reverse proxy for public exposure | Chosen for private/admin access | 2026-07-11 |
| Caddy | [docs](./ingress/caddy) | ⚫ Inactive | ~30–50 MB | Reverse proxy with automatic HTTPS by default | Documented alternative to Traefik; best outside Kubernetes | 2026-07-10 |

### Security

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| Secret Store | [docs](./security/secret-store) · [chart](../../helm-charts/infrastructure/platform/security/secret-store) · [config](./security/secret-store/terraform) | ⚫ Inactive | ~0.2–0.5 GB | Central vault for app secrets, tokens and accounts | Core before real apps | 2026-06-17 |
| External Secrets Operator | [docs](./security/external-secrets) · [chart](../../helm-charts/infrastructure/platform/security/external-secrets) · [config](./security/external-secrets/terraform) | ⚫ Inactive | ~50–100 MB | Syncs selected vault secrets into Kubernetes Secrets | GitOps standard | 2026-06-17 |
| Sealed Secrets | [docs](./security/sealed-secrets) · [chart](../../helm-charts/infrastructure/platform/security/sealed-secrets) · [config](./security/sealed-secrets/terraform) | ⚫ Inactive | ~50 MB | Encrypted Kubernetes Secrets stored in Git | Optional fallback | 2026-06-17 |
| Rights Management | [docs](./security/rights-management) | ⚫ Inactive | — | Identity, roles and app permission decisions (category) | Important later | 2026-06-17 |
| Keycloak | [docs](./security/rights-management/keycloak) · [chart](../../helm-charts/infrastructure/platform/security/rights-management/keycloak) · [config](./security/rights-management/keycloak/terraform) | ⚫ Inactive | ~0.7–1 GB | Identity provider for SSO, OIDC, OAuth2, users, groups and service accounts | Best first rights-management component | 2026-06-17 |
| Password Manager | [docs](./security/password-manager) | ⚫ Inactive | — | Human password vault, separate from application secrets (category) | High daily value | 2026-07-08 |
| Bitwarden (Vaultwarden) | [docs](./security/password-manager/bitwarden) · [chart](../../helm-charts/infrastructure/platform/security/password-manager/bitwarden) · [config](./security/password-manager/bitwarden/terraform) | ⚫ Inactive | ~50–100 MB | Family password manager (Vaultwarden server, Bitwarden clients) | Chosen password manager | 2026-07-08 |

### Storage

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| Longhorn | [docs](./storage/longhorn) · [chart](../../helm-charts/infrastructure/platform/storage/longhorn) · [config](./storage/longhorn/terraform) | ⚫ Inactive | ~0.3–0.5 GB / node | Persistent volumes for stateful Kubernetes workloads | Storage standard | 2026-06-17 |
| MinIO | [docs](./storage/minio) · [chart](../../helm-charts/infrastructure/platform/storage/minio) · [config](./storage/minio/terraform) | ⚫ Inactive | ~0.2–0.5 GB | The homelab S3 bucket equivalent for object storage | Homelab S3 standard | 2026-06-17 |

### Databases And Data Stores

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| PostgreSQL | [docs](./databases/postgresql) · [chart](../../helm-charts/infrastructure/platform/databases/postgresql) · [config](./databases/postgresql/terraform) | ⚫ Inactive | ~0.1–0.3 GB | Main SQL database for most custom services | Default database | 2026-06-17 |
| MySQL | [docs](./databases/mysql) · [chart](../../helm-charts/infrastructure/platform/databases/mysql) · [config](./databases/mysql/terraform) | ⚫ Inactive | ~0.3–0.5 GB | SQL database for MySQL-compatible apps and learning | Useful compatibility | 2026-06-17 |
| MongoDB | [docs](./databases/mongodb) · [chart](../../helm-charts/infrastructure/platform/databases/mongodb) · [config](./databases/mongodb/terraform) | ⚫ Inactive | ~0.3–1 GB | Document database for JSON-shaped data | Useful learning target | 2026-06-17 |
| Redis | [docs](./databases/redis) · [chart](../../helm-charts/infrastructure/platform/databases/redis) · [config](./databases/redis/terraform) | ⚫ Inactive | ~30–100 MB | Fast cache, session store and lightweight key-value system | Add when apps need it | 2026-06-17 |
| InfluxDB | [docs](./databases/influxdb) · [chart](../../helm-charts/infrastructure/platform/databases/influxdb) · [config](./databases/influxdb/terraform) | ⚫ Inactive | ~0.2–0.5 GB | Time-series database for sensors and measurements | Optional/specialized | 2026-06-17 |

### Messaging

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| NATS | [docs](./messaging/nats) · [chart](../../helm-charts/infrastructure/platform/messaging/nats) · [config](./messaging/nats/terraform) | ⚫ Inactive | ~20–50 MB | Lightweight event bus for simple service communication | Best first messaging choice | 2026-06-17 |
| RabbitMQ | [docs](./messaging/rabbitmq) · [chart](../../helm-charts/infrastructure/platform/messaging/rabbitmq) · [config](./messaging/rabbitmq/terraform) | ⚫ Inactive | ~0.15–0.3 GB | Message broker for queues, retries and workers | Use for job queues | 2026-06-17 |
| Kafka | [docs](./messaging/kafka) · [chart](../../helm-charts/infrastructure/platform/messaging/kafka) · [config](./messaging/kafka/terraform) | ⚫ Inactive | ~1–2 GB+ | Durable event log for replayable streams | Advanced/later | 2026-06-17 |

### API Platform

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| GraphQL | [docs](./api/graphql) · [chart](../../helm-charts/infrastructure/platform/api/graphql) · [config](./api/graphql/terraform) | ⚫ Inactive | ~0.1–0.3 GB | API layer that combines data for clients and dashboards | Optional/app-driven | 2026-06-17 |

### Observability

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| Prometheus | [docs](./observability/metrics/prometheus) · [chart](../../helm-charts/infrastructure/platform/observability/metrics/prometheus) · [config](./observability/metrics/prometheus/terraform) | ⚫ Inactive | ~0.5–1 GB+ | Metrics database and alerting engine | Observability standard | 2026-06-17 |
| Grafana | [docs](./observability/metrics/grafana) · [chart](../../helm-charts/infrastructure/platform/observability/metrics/grafana) · [config](./observability/metrics/grafana/terraform) | ⚫ Inactive | ~0.15–0.3 GB | Dashboard UI for metrics, logs and traces | Observability standard | 2026-06-17 |
| OpenSearch | [docs](./observability/logging/opensearch) · [chart](../../helm-charts/infrastructure/platform/observability/logging/opensearch) · [config](./observability/logging/opensearch/terraform) | ⚫ Inactive | ~2–4 GB+ | Search engine for logs and analytics | Optional/heavy | 2026-06-17 |
| Fluent Bit | [docs](./observability/logging/fluent-bit) · [chart](../../helm-charts/infrastructure/platform/observability/logging/fluent-bit) · [config](./observability/logging/fluent-bit/terraform) | ⚫ Inactive | ~30–50 MB / node | Lightweight log collector for Kubernetes nodes | Logging standard | 2026-06-17 |
| OpenTelemetry Collector | [docs](./observability/tracing/opentelemetry-collector) · [chart](../../helm-charts/infrastructure/platform/observability/tracing/opentelemetry-collector) · [config](./observability/tracing/opentelemetry-collector/terraform) | ⚫ Inactive | ~0.1–0.2 GB | Neutral pipeline for traces, metrics and logs | Modern standard | 2026-06-17 |
| Jaeger | [docs](./observability/tracing/jaeger) · [chart](../../helm-charts/infrastructure/platform/observability/tracing/jaeger) · [config](./observability/tracing/jaeger/terraform) | ⚫ Inactive | ~0.2–0.5 GB | Trace UI/backend for distributed services | Good first tracing backend | 2026-06-17 |
| Zipkin | [docs](./observability/tracing/zipkin) · [chart](../../helm-charts/infrastructure/platform/observability/tracing/zipkin) · [config](./observability/tracing/zipkin/terraform) | ⚫ Inactive | ~0.3–0.5 GB | Simpler tracing backend and compatibility target | Mostly optional | 2026-06-17 |

### Backup

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| Velero | [docs](./backup/velero) · [chart](../../helm-charts/infrastructure/platform/backup/velero) · [config](./backup/velero/terraform) | ⚫ Inactive | ~0.1–0.2 GB | Backup and restore tool for Kubernetes resources and volumes | Important before real data | 2026-06-17 |

### Registry

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| Harbor | [docs](./registry/harbor) · [chart](../../helm-charts/infrastructure/platform/registry/harbor) · [config](./registry/harbor/terraform) | ⚫ Inactive | ~1–2 GB | Private container registry for images and OCI artifacts | Good container standard | 2026-06-17 |
| Artifact Repository (Nexus) | [docs](./registry/artifact-repository) · [chart](../../helm-charts/infrastructure/platform/registry/artifact-repository) · [config](./registry/artifact-repository/terraform) | ⚫ Inactive | ~1.5–2.5 GB | Private package registry for Docker, npm, NuGet and artifacts | Homelab: Nexus, business: Artifactory | 2026-06-17 |

### Runtime

| Name | Path | Status | Idle RAM | What it is | Recommendation | Last update |
|---|---|---|---|---|---|---|
| Dapr | [docs](./runtime/dapr) · [chart](../../helm-charts/infrastructure/platform/runtime/dapr) · [config](./runtime/dapr/terraform) | ⚫ Inactive | ~0.3 GB + ~50 MB sidecar / app | App runtime for pub/sub, state, secrets and service calls | Useful after custom services | 2026-06-17 |
| Service Mesh | [docs](./runtime/service-mesh) · [chart](../../helm-charts/infrastructure/platform/runtime/service-mesh) · [config](./runtime/service-mesh/terraform) | ⚫ Inactive | ~0.5–1 GB + sidecars | Traffic security and control between services | Usually later | 2026-06-17 |

---

## Recommended Baseline

For the first serious build, keep the always-running baseline small:

- Traefik and cert-manager once the first service is exposed
- AdGuard Home + CoreDNS once devices should use homelab names
- Longhorn for distributed block storage
- PostgreSQL as the primary database; Redis once an application needs caching
- Prometheus and Grafana once there is something to observe
- Velero before any data becomes irreplaceable

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
