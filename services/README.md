# Services

[<- Back to Repository Overview](../README.md)

This directory is for custom services built specifically for this homelab.

It is intentionally separate from [`../infrastructure`](../infrastructure). Infrastructure documents the platform this project runs on. Services are the applications, APIs, workers and operators that run on top of that platform.

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

These belong under [`../infrastructure`](../infrastructure):

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
../infrastructure/kubernetes/messaging/nats/
```

The NATS documentation stays in infrastructure because NATS is a shared platform component.

---

## Planned Service Layout

```text
services/
├── README.md
├── hardware-event-api/
├── node-control-api/
├── cluster-admin-api/
├── dashboard-bff/
└── operators/
```

Potential future services:

| Service | Purpose |
|---|---|
| `hardware-event-api` | Publishes hardware and node events to the messaging layer |
| `node-control-api` | Controls power, reboot and maintenance actions through Intel vPro or similar hardware APIs |
| `cluster-admin-api` | Provides backend operations for the admin dashboard |
| `dashboard-bff` | Backend-for-frontend for web or mobile dashboards |
| `operators/*` | Custom Kubernetes operators built for this homelab |

---

## Rule Of Thumb

If it is a product installed into the cluster, document it in `infrastructure`.

If it is code written for this homelab, put it in `services`.

If a custom service becomes large enough to deserve its own repository, keep a short README here and link to the external repo.
