# Databases

[<- Back to Kubernetes](../README.md)

This directory documents shared database systems that may run inside the cluster.

Running databases on Kubernetes is useful for learning, but it is also one of the fastest ways to discover whether storage, backups and observability are actually working.

---

## Database And Data Store Catalog

| System | Status | Purpose | Documentation |
|---|---|---|---|
| PostgreSQL | ⚫ Inactive | Primary relational database and default choice for new services | [postgresql](./postgresql) |
| MySQL | ⚫ Inactive | Compatibility with common web stacks and MySQL-specific tooling | [mysql](./mysql) |
| MongoDB | ⚫ Inactive | Document database for JSON-heavy workloads and experiments | [mongodb](./mongodb) |
| Redis | ⚫ Inactive | Cache, key-value store, session storage and lightweight queues | [redis](./redis) |
| InfluxDB | ⚫ Inactive | Time-series data and sensor-style measurements | [influxdb](./influxdb) |

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
