# Kubernetes Infrastructure

[<- Back to Infrastructure](../README.md)

This directory is the main catalog for Kubernetes platform components used or evaluated in this homelab.

It covers cluster bootstrap, GitOps, networking, security, storage, databases, messaging, APIs, observability, backups, registries, runtimes, user-facing applications and operators. Deployment manifests do not live here. The future deployment source of truth should live under [`../../helm-charts`](../../helm-charts), while this directory explains why each component exists and how it should be operated.

Kubernetes is a platform for running containers across a group of machines. It schedules workloads, restarts failed containers, exposes services, mounts storage and provides a declarative API for infrastructure automation.

Kubernetes by itself is not the whole platform. A useful cluster also needs networking, ingress, TLS, storage, secrets, databases, observability, backups, registries and deployment workflows. This directory is the map of those platform building blocks.

For beginners, read this catalog as a set of layers, not as an installation checklist. Cilium and bootstrap are foundational. Kafka, service mesh and OpenSearch are advanced or workload-dependent. The right cluster is the smallest one that teaches the target concepts and supports the real applications.

---

## How To Read This Catalog

Each component page should explain the concept first and the project decision second. The docs intentionally include alternatives and weaknesses because a homelab should teach decision-making, not only tool names.

Use the status and recommendation columns as guidance:

- `Unavoidable`: required for the cluster or this repository structure to work.
- `Standard`: common default in Kubernetes or platform engineering.
- `Recommended`: strong first choice for this homelab.
- `Optional`: useful when a workload needs it.
- `Advanced/later`: valuable learning target, but not an early dependency.

---

## Directory Layout

```text
kubernetes/
├── api/
│   └── graphql/
├── applications/
│   ├── nextcloud/
│   └── plex/
├── backup/
│   └── velero/
├── bootstrap/
├── databases/
│   ├── influxdb/
│   ├── mongodb/
│   ├── mysql/
│   ├── postgresql/
│   └── redis/
├── gitops/
│   ├── argocd/
│   └── flux/
├── messaging/
│   ├── kafka/
│   ├── nats/
│   └── rabbitmq/
├── networking/
│   ├── cert-manager/
│   ├── cilium/
│   ├── ingress/
│   ├── metallb/
│   └── traefik/
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
├── operators/
├── registry/
│   ├── artifact-repository/
│   └── harbor/
├── runtime/
│   ├── dapr/
│   └── service-mesh/
├── security/
│   ├── external-secrets/
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

Status meanings:

- `🟢 Active`: currently deployed or actively operated in the cluster
- `⚫ Inactive`: documented, planned or available for future use, but not currently running

Current state: every component is `⚫ Inactive` until the cluster build starts.

Do not read this catalog as an installation checklist. It is a map of possible platform building blocks. Start with the unavoidable cluster pieces, add the recommended standards when they solve a real problem, and keep advanced or specialized systems inactive until there is a workload or learning goal for them.

The first link in each catalog row points to the local documentation. The second link points to the planned Helm chart location. Most chart directories are intentionally still empty or not created yet.

Recommendation meanings:

- `Unavoidable`: needed for the cluster or this repository structure to make sense
- `Standard`: a common default for this layer
- `Recommended`: good first choice for this homelab
- `Optional`: useful only when a workload needs it
- `Advanced/later`: interesting, but not an early dependency

### Bootstrap

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./bootstrap](./bootstrap)<br>[../../helm-charts/bootstrap](../../helm-charts/bootstrap) | ⚫ Inactive | The first process that creates the Kubernetes cluster | Unavoidable | 2026-06-17 |

### GitOps

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./gitops/flux](./gitops/flux)<br>[../../helm-charts/gitops/flux](../../helm-charts/gitops/flux) | ⚫ Inactive | GitOps controller that keeps the cluster synced from Git | Recommended standard | 2026-06-17 |
| [./gitops/argocd](./gitops/argocd)<br>[../../helm-charts/gitops/argocd](../../helm-charts/gitops/argocd) | ⚫ Inactive | GitOps platform with a strong visual application UI | Optional alternative | 2026-06-17 |

### Networking

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./networking/cilium](./networking/cilium)<br>[../../helm-charts/networking/cilium](../../helm-charts/networking/cilium) | ⚫ Inactive | The pod network layer for Kubernetes | Unavoidable CNI choice | 2026-06-17 |
| [./networking/metallb](./networking/metallb)<br>[../../helm-charts/networking/metallb](../../helm-charts/networking/metallb) | ⚫ Inactive | LoadBalancer IP provider for bare-metal clusters | Bare-metal standard | 2026-06-17 |
| [./networking/traefik](./networking/traefik)<br>[../../helm-charts/networking/traefik](../../helm-charts/networking/traefik) | ⚫ Inactive | Reverse proxy that exposes HTTP(S) services | Homelab standard | 2026-06-17 |
| [./networking/ingress](./networking/ingress)<br>[../../helm-charts/networking/ingress](../../helm-charts/networking/ingress) | ⚫ Inactive | The general HTTP(S) entrypoint concept | Required once apps are exposed | 2026-06-17 |
| [./networking/cert-manager](./networking/cert-manager)<br>[../../helm-charts/networking/cert-manager](../../helm-charts/networking/cert-manager) | ⚫ Inactive | Automatic TLS certificate management | Strongly recommended | 2026-06-17 |

### Security

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./security/secret-store](./security/secret-store)<br>[../../helm-charts/security/secret-store](../../helm-charts/security/secret-store) | ⚫ Inactive | Central vault for app secrets, tokens and accounts | Core before real apps | 2026-06-17 |
| [./security/external-secrets](./security/external-secrets)<br>[../../helm-charts/security/external-secrets](../../helm-charts/security/external-secrets) | ⚫ Inactive | Syncs selected vault secrets into Kubernetes Secrets | GitOps standard | 2026-06-17 |
| [./security/sealed-secrets](./security/sealed-secrets)<br>[../../helm-charts/security/sealed-secrets](../../helm-charts/security/sealed-secrets) | ⚫ Inactive | Encrypted Kubernetes Secrets stored in Git | Optional fallback | 2026-06-17 |
| [./security/rights-management](./security/rights-management)<br>[../../helm-charts/security/rights-management](../../helm-charts/security/rights-management) | ⚫ Inactive | Identity, roles and app permission decisions | Important later | 2026-06-17 |
| [./security/rights-management/keycloak](./security/rights-management/keycloak)<br>[../../helm-charts/security/rights-management/keycloak](../../helm-charts/security/rights-management/keycloak) | ⚫ Inactive | Identity provider for SSO, OIDC, OAuth2, users, groups and service accounts | Best first rights-management component | 2026-06-17 |

### Storage

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./storage/longhorn](./storage/longhorn)<br>[../../helm-charts/storage/longhorn](../../helm-charts/storage/longhorn) | ⚫ Inactive | Persistent volumes for stateful Kubernetes workloads | Storage standard | 2026-06-17 |
| [./storage/minio](./storage/minio)<br>[../../helm-charts/storage/minio](../../helm-charts/storage/minio) | ⚫ Inactive | The homelab S3 bucket equivalent for object storage | Homelab S3 standard | 2026-06-17 |

### Databases And Data Stores

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./databases/postgresql](./databases/postgresql)<br>[../../helm-charts/databases/postgresql](../../helm-charts/databases/postgresql) | ⚫ Inactive | Main SQL database for most custom services | Default database | 2026-06-17 |
| [./databases/mysql](./databases/mysql)<br>[../../helm-charts/databases/mysql](../../helm-charts/databases/mysql) | ⚫ Inactive | SQL database for MySQL-compatible apps and learning | Useful compatibility | 2026-06-17 |
| [./databases/mongodb](./databases/mongodb)<br>[../../helm-charts/databases/mongodb](../../helm-charts/databases/mongodb) | ⚫ Inactive | Document database for JSON-shaped data | Useful learning target | 2026-06-17 |
| [./databases/redis](./databases/redis)<br>[../../helm-charts/databases/redis](../../helm-charts/databases/redis) | ⚫ Inactive | Fast cache, session store and lightweight key-value system | Add when apps need it | 2026-06-17 |
| [./databases/influxdb](./databases/influxdb)<br>[../../helm-charts/databases/influxdb](../../helm-charts/databases/influxdb) | ⚫ Inactive | Time-series database for sensors and measurements | Optional/specialized | 2026-06-17 |

### Messaging

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./messaging/nats](./messaging/nats)<br>[../../helm-charts/messaging/nats](../../helm-charts/messaging/nats) | ⚫ Inactive | Lightweight event bus for simple service communication | Best first messaging choice | 2026-06-17 |
| [./messaging/rabbitmq](./messaging/rabbitmq)<br>[../../helm-charts/messaging/rabbitmq](../../helm-charts/messaging/rabbitmq) | ⚫ Inactive | Message broker for queues, retries and workers | Use for job queues | 2026-06-17 |
| [./messaging/kafka](./messaging/kafka)<br>[../../helm-charts/messaging/kafka](../../helm-charts/messaging/kafka) | ⚫ Inactive | Durable event log for replayable streams | Advanced/later | 2026-06-17 |

### API Platform

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./api/graphql](./api/graphql)<br>[../../helm-charts/api/graphql](../../helm-charts/api/graphql) | ⚫ Inactive | API layer that combines data for clients and dashboards | Optional/app-driven | 2026-06-17 |

### Observability

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./observability/metrics/prometheus](./observability/metrics/prometheus)<br>[../../helm-charts/observability/prometheus](../../helm-charts/observability/prometheus) | ⚫ Inactive | Metrics database and alerting engine | Observability standard | 2026-06-17 |
| [./observability/metrics/grafana](./observability/metrics/grafana)<br>[../../helm-charts/observability/grafana](../../helm-charts/observability/grafana) | ⚫ Inactive | Dashboard UI for metrics, logs and traces | Observability standard | 2026-06-17 |
| [./observability/logging/opensearch](./observability/logging/opensearch)<br>[../../helm-charts/observability/opensearch](../../helm-charts/observability/opensearch) | ⚫ Inactive | Search engine for logs and analytics | Optional/heavy | 2026-06-17 |
| [./observability/logging/fluent-bit](./observability/logging/fluent-bit)<br>[../../helm-charts/observability/fluent-bit](../../helm-charts/observability/fluent-bit) | ⚫ Inactive | Lightweight log collector for Kubernetes nodes | Logging standard | 2026-06-17 |
| [./observability/tracing/opentelemetry-collector](./observability/tracing/opentelemetry-collector)<br>[../../helm-charts/observability/opentelemetry-collector](../../helm-charts/observability/opentelemetry-collector) | ⚫ Inactive | Neutral pipeline for traces, metrics and logs | Modern standard | 2026-06-17 |
| [./observability/tracing/jaeger](./observability/tracing/jaeger)<br>[../../helm-charts/observability/jaeger](../../helm-charts/observability/jaeger) | ⚫ Inactive | Trace UI/backend for distributed services | Good first tracing backend | 2026-06-17 |
| [./observability/tracing/zipkin](./observability/tracing/zipkin)<br>[../../helm-charts/observability/zipkin](../../helm-charts/observability/zipkin) | ⚫ Inactive | Simpler tracing backend and compatibility target | Mostly optional | 2026-06-17 |

### Backup

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./backup/velero](./backup/velero)<br>[../../helm-charts/backup/velero](../../helm-charts/backup/velero) | ⚫ Inactive | Backup and restore tool for Kubernetes resources and volumes | Important before real data | 2026-06-17 |

### Registry

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./registry/harbor](./registry/harbor)<br>[../../helm-charts/registry/harbor](../../helm-charts/registry/harbor) | ⚫ Inactive | Private container registry for images and OCI artifacts | Good container standard | 2026-06-17 |
| [./registry/artifact-repository](./registry/artifact-repository)<br>[../../helm-charts/registry/artifact-repository](../../helm-charts/registry/artifact-repository) | ⚫ Inactive | Private package registry for Docker, npm, NuGet and artifacts | Homelab: Nexus, business: Artifactory | 2026-06-17 |

### Runtime

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./runtime/dapr](./runtime/dapr)<br>[../../helm-charts/runtime/dapr](../../helm-charts/runtime/dapr) | ⚫ Inactive | App runtime for pub/sub, state, secrets and service calls | Useful after custom services | 2026-06-17 |
| [./runtime/service-mesh](./runtime/service-mesh)<br>[../../helm-charts/runtime/service-mesh](../../helm-charts/runtime/service-mesh) | ⚫ Inactive | Traffic security and control between services | Usually later | 2026-06-17 |

### Applications

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./applications/nextcloud](./applications/nextcloud)<br>[../../helm-charts/applications/nextcloud](../../helm-charts/applications/nextcloud) | ⚫ Inactive | Self-hosted file sync, sharing and productivity app | Good user-facing homelab app | 2026-06-17 |
| [./applications/plex](./applications/plex)<br>[../../helm-charts/applications/plex](../../helm-charts/applications/plex) | ⚫ Inactive | Self-hosted media server for movies, shows and music | Optional/lifestyle app | 2026-06-17 |

### Operators

| Path | Status | What it is | Recommendation | Last update |
|---|---|---|---|---|
| [./operators](./operators)<br>[../../helm-charts/operators](../../helm-charts/operators) | ⚫ Inactive | Controllers that automate lifecycle of complex software | Use selectively | 2026-06-17 |

---

## Recommended Baseline

For the first serious Kubernetes build, keep the always-running baseline small:

- Cilium for CNI, NetworkPolicy and future eBPF learning
- MetalLB for bare-metal LoadBalancer services
- one ingress controller
- cert-manager for certificate automation
- Longhorn for distributed block storage
- Flux or another GitOps controller once deployments become repeatable
- PostgreSQL, MySQL and MongoDB as the primary learning databases
- Redis once an application needs caching, sessions or lightweight queue patterns

Everything else can be added when there is a real workload or learning goal. This keeps the cluster understandable and avoids turning the first build into a permanent maintenance queue.

---

## Deployment Rule

This directory answers:

- What is the component?
- Why does this project care?
- Should it run all the time?
- What are the main alternatives?
- What should be monitored?

Deployment files should be linked from future paths such as:

```text
../../helm-charts/<component>/
../../helm-charts/networking/<component>/
../../helm-charts/applications/<application>/
../../helm-charts/databases/<component>/
../../helm-charts/storage/<component>/
../../helm-charts/security/rights-management/keycloak/
```

---

## Learning Links

- [Wikipedia: Kubernetes](https://en.wikipedia.org/wiki/Kubernetes)
- [Kubernetes concepts documentation](https://kubernetes.io/docs/concepts/)
- [Wikipedia: Containerization](https://en.wikipedia.org/wiki/OS-level_virtualization)
- [Wikipedia: Microservices](https://en.wikipedia.org/wiki/Microservices)
- [Wikipedia: DevOps](https://en.wikipedia.org/wiki/DevOps)
