# Services

[<- Back to Repository Overview](../README.md)

This directory is for custom services built specifically for this homelab.

It is intentionally separate from [`kubernetes`](../infrastructure/kubernetes) and [`platform`](../infrastructure/platform). Those directories document the cluster and the shared services this project runs on. Services are the custom applications, APIs, workers and operators built for this homelab on top of that platform.

---

## What Belongs Here

Use this directory for code and service-level documentation such as:

- Go microservices
- REST APIs
- GraphQL gateways implemented by this project
- background workers
- hardware automation APIs
- custom Kubernetes operators
- service-specific Dockerfiles
- service-specific tests
- service-specific runtime configuration examples

---

## What Does Not Belong Here

Do not put shared platform products here.

These belong under [`platform`](../infrastructure/platform):

- PostgreSQL
- MySQL
- MongoDB
- Redis
- NATS
- RabbitMQ
- Kafka
- Traefik
- MinIO
- Dapr
- Prometheus
- Grafana
- Secret Store
- Artifact Repository

Those are dependencies or platform services. They are not custom application services owned by this repository.

---

## Relationship To Infrastructure

A service may depend on infrastructure, but it should not own the infrastructure documentation.

Example:

```text
services/hardware-event-api/
├── README.md
├── src/
├── Dockerfile
└── tests/
```

If that service publishes events to NATS, its README should link to:

```text
../infrastructure/platform/messaging/nats/
```

The NATS documentation stays under `platform` because NATS is a shared platform component.

---

## Planned Service Layout

```text
services/
├── README.md
├── hardware-event-api/
├── node-control-api/
├── cluster-admin-api/
├── dashboard-bff/
├── responder/
└── operators/
```

Potential future services (`Runs on`: `k8s` = cluster workload, `pve` = guest on the Proxmox host):

| Service | Runs on | Purpose |
|---|---|---|
| `cluster-admin-api` | k8s | Provides backend operations for the admin dashboard |
| `dashboard-bff` | k8s | Backend-for-frontend for web or mobile dashboards |
| `hardware-event-api` | k8s | Publishes hardware and node events to the messaging layer |
| `node-control-api` | k8s | Controls power, reboot and maintenance actions through Intel vPro or similar hardware APIs |
| `operators/*` | k8s | Custom Kubernetes operators built for this homelab |
| `responder` | lxc + k8s | Cross-watchdog: the LXC instance monitors the k8s nodes, the cluster instance monitors the Proxmox host — each can alert and revive the other world via Intel vPro. Neither world watches itself. |

---

## Rule Of Thumb

If it is a product installed into the cluster, document it in `infrastructure`.

If it is code written for this homelab, put it in `services`.

If a custom service becomes large enough to deserve its own repository, keep a short README here and link to the external repo.
