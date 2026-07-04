# Databases

[<- Back to Kubernetes](../README.md)

This directory documents shared database systems that may run inside the cluster.

Running databases on Kubernetes is useful for learning, but it is also one of the fastest ways to discover whether storage, backups and observability are actually working.

A database stores state that must survive application restarts. That state can be relational rows, JSON documents, cache entries, time-series measurements or short-lived coordination data.

Databases are different from stateless web applications. If a web pod crashes, Kubernetes can start another one. If a database loses its data, the application may lose users, files, settings, history or business records. That is why databases force the platform to care about storage, backups, restore tests, upgrades and monitoring.

This directory includes several database categories because they solve different problems. PostgreSQL and MySQL are relational databases. MongoDB is a document database. Redis is an in-memory key-value store often used for caching and sessions. InfluxDB is a time-series database for timestamped measurements.

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

## Data Model Guide

| Model | Best fit | Example |
|---|---|---|
| Relational | Structured data with relationships and transactions | Users, roles, orders, audit logs |
| Document | JSON-like records with flexible shape | Device metadata, nested configuration, denormalized views |
| Key-value/cache | Fast lookup and short-lived state | Sessions, rate limits, cached summaries |
| Time-series | Measurements indexed by time | Power usage, temperatures, sensor readings |

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

---

## Learning Links

- [Wikipedia: Database](https://en.wikipedia.org/wiki/Database)
- [Wikipedia: Relational database](https://en.wikipedia.org/wiki/Relational_database)
- [Wikipedia: NoSQL](https://en.wikipedia.org/wiki/NoSQL)
- [Wikipedia: Time series database](https://en.wikipedia.org/wiki/Time_series_database)
- [Kubernetes StatefulSet documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
