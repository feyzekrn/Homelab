# Databases

[<- Back to Platform](../README.md)

This directory documents the database systems used across the homelab — **in both worlds**, not only on the cluster.

Running databases on Kubernetes is useful for learning, and it is also one of the fastest ways to discover whether storage, backups and observability are actually working. But not every database here belongs on the cluster, and where each one runs follows from what it serves:

| Instance | Runs on | Serves |
|---|---|---|
| Cluster PostgreSQL / Redis | `k8s` | Custom services and cluster workloads |
| Identity PostgreSQL | `lxc` on `pve0` | [Keycloak](../security/rights-management/keycloak) — must outlive a cluster rebuild |
| Per-app databases | inside each app's `lxc` | [Nextcloud](../../../applications/nextcloud), [Immich](../../../applications/immich) |

The rule behind the split is the same one used everywhere in this catalog: **a database lives where the thing it serves lives.** Sharing one instance across both worlds would be tidier and would quietly create the dependency that the two-world architecture exists to avoid.

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

| Name | Path | Status | Runs on | Idle RAM | Purpose |
|---|---|---|---|---|
| PostgreSQL | [docs](./postgresql) · [chart](../../../helm-charts/infrastructure/platform/databases/postgresql) · [config](./postgresql/terraform) | ⚫ Inactive | k8s | ~0.1–0.3 GB | **Chosen default** — primary relational database for new services |
| Redis | [docs](./redis) · [chart](../../../helm-charts/infrastructure/platform/databases/redis) · [config](./redis/terraform) | ⚫ Inactive | k8s | ~30–100 MB | **Chosen cache** — deployed once an application needs it |
| MySQL | [docs](./mysql) | ⚫ Inactive | — | ~0.3–0.5 GB | Documented alternative — compatibility with MySQL-only applications |
| MongoDB | [docs](./mongodb) | ⚫ Inactive | — | ~0.3–1 GB | Documented — deploy only when a workload genuinely needs documents |
| InfluxDB | [docs](./influxdb) | ⚫ Inactive | — | ~0.2–0.5 GB | Documented — Prometheus already covers metrics and sensor history |

**One database until proven otherwise.** PostgreSQL handles relational data, JSON documents and time-series well enough for everything planned here, and every additional engine means another backup path, another upgrade cycle and another set of failure modes. The alternatives stay documented so the decision can be revisited with a concrete reason — not because variety is a goal.

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
