# Kubernetes Infrastructure

[<- Back to Infrastructure](../README.md)

This directory is the main catalog for Kubernetes platform components used or evaluated in this homelab.

It covers cluster bootstrap, GitOps, networking, security, storage, databases, messaging, APIs, observability, backups, registries, runtimes and operators. Deployment manifests do not live here. The future deployment source of truth should live under [`../../helm-charts`](../../helm-charts), while this directory explains why each component exists and how it should be operated.

---

## Service Catalog

Status meanings:

- `🟢 Active`: currently deployed or actively operated in the cluster
- `⚫ Inactive`: documented, planned or available for future use, but not currently running

Current state: every component is `⚫ Inactive` until the cluster build starts.

Do not read this catalog as an installation checklist. It is a map of possible platform building blocks. Start with the unavoidable cluster pieces, add the recommended standards when they solve a real problem, and keep advanced or specialized systems inactive until there is a workload or learning goal for them.

Recommendation meanings:

- `Unavoidable`: needed for the cluster or this repository structure to make sense
- `Standard`: a common default for this layer
- `Recommended`: good first choice for this homelab
- `Optional`: useful only when a workload needs it
- `Advanced/later`: interesting, but not an early dependency

### Bootstrap

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| Cluster bootstrap | ⚫ Inactive | The first process that creates the Kubernetes cluster | Unavoidable | 2026-06-17 | [bootstrap](./bootstrap) | [bootstrap](../../helm-charts/bootstrap) |

### GitOps

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| Flux | ⚫ Inactive | GitOps controller that keeps the cluster synced from Git | Recommended standard | 2026-06-17 | [flux](./gitops/flux) | [flux](../../helm-charts/gitops/flux) |
| Argo CD | ⚫ Inactive | GitOps platform with a strong visual application UI | Optional alternative | 2026-06-17 | [argocd](./gitops/argocd) | [argocd](../../helm-charts/gitops/argocd) |

### Networking

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| Cilium | ⚫ Inactive | The pod network layer for Kubernetes | Unavoidable CNI choice | 2026-06-17 | [cilium](./networking/cilium) | [cilium](../../helm-charts/networking/cilium) |
| MetalLB | ⚫ Inactive | LoadBalancer IP provider for bare-metal clusters | Bare-metal standard | 2026-06-17 | [metallb](./networking/metallb) | [metallb](../../helm-charts/networking/metallb) |
| Traefik | ⚫ Inactive | Reverse proxy that exposes HTTP(S) services | Homelab standard | 2026-06-17 | [traefik](./networking/traefik) | [traefik](../../helm-charts/networking/traefik) |
| Ingress controller | ⚫ Inactive | The general HTTP(S) entrypoint concept | Required once apps are exposed | 2026-06-17 | [ingress](./networking/ingress) | [ingress](../../helm-charts/networking/ingress) |
| cert-manager | ⚫ Inactive | Automatic TLS certificate management | Strongly recommended | 2026-06-17 | [cert-manager](./networking/cert-manager) | [cert-manager](../../helm-charts/networking/cert-manager) |

### Security

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| Secret Store | ⚫ Inactive | Central vault for app secrets, tokens and accounts | Core before real apps | 2026-06-17 | [secret-store](./security/secret-store) | [secret-store](../../helm-charts/security/secret-store) |
| External Secrets Operator | ⚫ Inactive | Syncs selected vault secrets into Kubernetes Secrets | GitOps standard | 2026-06-17 | [external-secrets](./security/external-secrets) | [external-secrets](../../helm-charts/security/external-secrets) |
| Sealed Secrets | ⚫ Inactive | Encrypted Kubernetes Secrets stored in Git | Optional fallback | 2026-06-17 | [sealed-secrets](./security/sealed-secrets) | [sealed-secrets](../../helm-charts/security/sealed-secrets) |
| Rights Management | ⚫ Inactive | Identity, roles and app permission decisions | Important later | 2026-06-17 | [rights-management](./security/rights-management) | [rights-management](../../helm-charts/security/rights-management) |

### Storage

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| Longhorn | ⚫ Inactive | Persistent volumes for stateful Kubernetes workloads | Storage standard | 2026-06-17 | [longhorn](./storage/longhorn) | [longhorn](../../helm-charts/storage/longhorn) |
| MinIO | ⚫ Inactive | The homelab S3 bucket equivalent for object storage | Homelab S3 standard | 2026-06-17 | [minio](./storage/minio) | [minio](../../helm-charts/storage/minio) |

### Databases And Data Stores

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| PostgreSQL | ⚫ Inactive | Main SQL database for most custom services | Default database | 2026-06-17 | [postgresql](./databases/postgresql) | [postgresql](../../helm-charts/databases/postgresql) |
| MySQL | ⚫ Inactive | SQL database for MySQL-compatible apps and learning | Useful compatibility | 2026-06-17 | [mysql](./databases/mysql) | [mysql](../../helm-charts/databases/mysql) |
| MongoDB | ⚫ Inactive | Document database for JSON-shaped data | Useful learning target | 2026-06-17 | [mongodb](./databases/mongodb) | [mongodb](../../helm-charts/databases/mongodb) |
| Redis | ⚫ Inactive | Fast cache, session store and lightweight key-value system | Add when apps need it | 2026-06-17 | [redis](./databases/redis) | [redis](../../helm-charts/databases/redis) |
| InfluxDB | ⚫ Inactive | Time-series database for sensors and measurements | Optional/specialized | 2026-06-17 | [influxdb](./databases/influxdb) | [influxdb](../../helm-charts/databases/influxdb) |

### Messaging

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| NATS | ⚫ Inactive | Lightweight event bus for simple service communication | Best first messaging choice | 2026-06-17 | [nats](./messaging/nats) | [nats](../../helm-charts/messaging/nats) |
| RabbitMQ | ⚫ Inactive | Message broker for queues, retries and workers | Use for job queues | 2026-06-17 | [rabbitmq](./messaging/rabbitmq) | [rabbitmq](../../helm-charts/messaging/rabbitmq) |
| Kafka | ⚫ Inactive | Durable event log for replayable streams | Advanced/later | 2026-06-17 | [kafka](./messaging/kafka) | [kafka](../../helm-charts/messaging/kafka) |

### API Platform

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| GraphQL gateway | ⚫ Inactive | API layer that combines data for clients and dashboards | Optional/app-driven | 2026-06-17 | [graphql](./api/graphql) | [graphql](../../helm-charts/api/graphql) |

### Observability

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| Prometheus | ⚫ Inactive | Metrics database and alerting engine | Observability standard | 2026-06-17 | [prometheus](./observability/metrics/prometheus) | [prometheus](../../helm-charts/observability/prometheus) |
| Grafana | ⚫ Inactive | Dashboard UI for metrics, logs and traces | Observability standard | 2026-06-17 | [grafana](./observability/metrics/grafana) | [grafana](../../helm-charts/observability/grafana) |
| OpenSearch stack | ⚫ Inactive | Search engine for logs and analytics | Optional/heavy | 2026-06-17 | [opensearch](./observability/logging/opensearch) | [opensearch](../../helm-charts/observability/opensearch) |
| Fluent Bit | ⚫ Inactive | Lightweight log collector for Kubernetes nodes | Logging standard | 2026-06-17 | [fluent-bit](./observability/logging/fluent-bit) | [fluent-bit](../../helm-charts/observability/fluent-bit) |
| OpenTelemetry Collector | ⚫ Inactive | Neutral pipeline for traces, metrics and logs | Modern standard | 2026-06-17 | [opentelemetry-collector](./observability/tracing/opentelemetry-collector) | [opentelemetry-collector](../../helm-charts/observability/opentelemetry-collector) |
| Jaeger | ⚫ Inactive | Trace UI/backend for distributed services | Good first tracing backend | 2026-06-17 | [jaeger](./observability/tracing/jaeger) | [jaeger](../../helm-charts/observability/jaeger) |
| Zipkin | ⚫ Inactive | Simpler tracing backend and compatibility target | Mostly optional | 2026-06-17 | [zipkin](./observability/tracing/zipkin) | [zipkin](../../helm-charts/observability/zipkin) |

### Backup

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| Velero | ⚫ Inactive | Backup and restore tool for Kubernetes resources and volumes | Important before real data | 2026-06-17 | [velero](./backup/velero) | [velero](../../helm-charts/backup/velero) |

### Registry

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| Harbor | ⚫ Inactive | Private container registry for images and OCI artifacts | Good container standard | 2026-06-17 | [harbor](./registry/harbor) | [harbor](../../helm-charts/registry/harbor) |
| Artifact Repository | ⚫ Inactive | Private package registry for Docker, npm, NuGet and artifacts | Homelab: Nexus, business: Artifactory | 2026-06-17 | [artifact-repository](./registry/artifact-repository) | [artifact-repository](../../helm-charts/registry/artifact-repository) |

### Runtime

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| Dapr | ⚫ Inactive | App runtime for pub/sub, state, secrets and service calls | Useful after custom services | 2026-06-17 | [dapr](./runtime/dapr) | [dapr](../../helm-charts/runtime/dapr) |
| Service mesh | ⚫ Inactive | Traffic security and control between services | Usually later | 2026-06-17 | [service-mesh](./runtime/service-mesh) | [service-mesh](../../helm-charts/runtime/service-mesh) |

### Operators

| Service | Status | What it is | Recommendation | Last update | Documentation | Helm charts |
|---|---|---|---|---|---|---|
| Operators | ⚫ Inactive | Controllers that automate lifecycle of complex software | Use selectively | 2026-06-17 | [operators](./operators) | [operators](../../helm-charts/operators) |

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
../../helm-charts/platform/<component>/
../../helm-charts/databases/<component>/
```
