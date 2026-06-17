# Databases

[<- Back to Kubernetes](../README.md)

This directory documents shared database systems that may run inside the cluster.

Running databases on Kubernetes is useful for learning, but it is also one of the fastest ways to discover whether storage, backups and observability are actually working.

---

## Why This Matters

Databases hold the state that applications care about. If they are unreliable, the rest of the platform does not matter. Running databases in Kubernetes teaches practical lessons about persistence, upgrades, backups, resource limits, monitoring and failure recovery.

In a homelab, databases are both useful and educational. PostgreSQL can back custom services, MySQL helps with ecosystem compatibility, MongoDB teaches document modeling, Redis covers caching and InfluxDB handles time-series measurements.

In companies, database operation is usually treated with strict ownership. Teams care about data durability, backup windows, restore tests, access control, migrations, performance and upgrade planning. The homelab should document those ideas at a smaller scale.

---

## What You Can Do With It

- store application data for custom services
- compare relational and document modeling
- test ORM and migration behavior
- add caching and sessions with Redis
- store sensor and hardware measurements
- practice backup and restore workflows
- learn when an operator is better than a hand-written StatefulSet

---

## Database And Data Store Catalog

| Path | Status | Purpose |
|---|---|---|
| [`./postgresql`](./postgresql) | ⚫ Inactive | Primary relational database and default choice for new services |
| [`./mysql`](./mysql) | ⚫ Inactive | Compatibility with common web stacks and MySQL-specific tooling |
| [`./mongodb`](./mongodb) | ⚫ Inactive | Document database for JSON-heavy workloads and experiments |
| [`./redis`](./redis) | ⚫ Inactive | Cache, key-value store, session storage and lightweight queues |
| [`./influxdb`](./influxdb) | ⚫ Inactive | Time-series data and sensor-style measurements |

---

## Baseline Rule

PostgreSQL should be the default relational database unless a workload specifically needs MySQL. MongoDB is useful when document modeling is part of the learning goal. Redis should be added when an application needs caching, sessions, rate limiting or short-lived coordination data.

Before storing important data, define:

- backup schedule
- restore process
- storage class
- resource requests and limits
- monitoring targets
- upgrade plan
