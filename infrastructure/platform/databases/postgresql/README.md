# PostgreSQL

[<- Back to Databases](../README.md)

PostgreSQL is the **chosen default relational database** for this homelab.

It is mature, widely used, strict enough to teach good data modeling and flexible enough for most full-stack applications.

**It runs more than once, deliberately.** One database engine, three deployments, three different reasons:

| Instance | Runs on | Serves | Why separate |
|---|---|---|---|
| Cluster PostgreSQL | `k8s` | Custom services, cluster workloads | The normal case — Longhorn volumes, backed up by Velero |
| Identity PostgreSQL | `lxc` on `pve0` | [Keycloak](../../security/rights-management/keycloak) only | Must survive a cluster rebuild, or the [anchor](../../../../setup/compute/README.md#the-bridge-one-node-with-a-foot-in-both-worlds) anchors nothing |
| Per-app databases | inside each `lxc` | [Nextcloud](../../../../applications/nextcloud), [Immich](../../../../applications/immich) | Each family app stays one self-contained `vzdump`; no shared outage takes all of them down |

Resisting the urge to run one shared database for everything is the point. A single instance would be tidier on paper and would create a dependency between every app on the machine — and in the identity case, a dependency that defeats the architecture.

PostgreSQL stores data in tables with rows, columns, constraints, indexes and transactions. It is a relational database, which means it is strong at representing structured data and relationships between data.

For example, users can belong to groups, groups can have roles, roles can grant permissions and audit logs can reference the user who performed an action. SQL lets applications query and join that data reliably.

PostgreSQL also supports JSONB, full-text search, extensions and advanced indexing, so it can handle many workloads that might otherwise require a separate specialized database.

---

## Why It Fits

PostgreSQL is the best default choice for new services because it handles relational data, JSON fields, indexing, migrations and transactional workloads well.

It is also a good teaching database. It rewards clear schemas, constraints, migrations and backup discipline. Those habits transfer well to professional backend development.

---

## Prerequisites

**Cluster instance:**

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../kubernetes/cilium) | It runs as pods |
| [Longhorn](../../storage/longhorn) | Database volumes must survive a pod moving between nodes |
| [Vault](../../security/secret-store) + [External Secrets](../../security/external-secrets) | Database passwords do not belong in a values file |
| [Velero](../../backup/velero) **plus** `pg_dump` | Volume snapshots are crash-consistent; a database-native dump is what actually restores cleanly |

**Identity instance on `pve0`:** only Proxmox VE — it is deliberately built before the cluster exists, so it has no cluster dependencies at all.

**One warning worth internalising:** a Longhorn snapshot of a running database is a crash-consistent copy, not a clean backup. It usually restores, and "usually" is not a word that belongs near the data everything else authenticates against. Schedule `pg_dump` alongside Velero rather than instead of it.

---

## Used For

- primary application databases
- admin dashboard backend data
- relational modeling practice
- migration tooling practice
- backup and restore testing
- JSONB experiments where limited document flexibility is useful

---

## Strengths

- Strong SQL and relational modeling.
- ACID transactions for reliable state changes.
- Rich indexing and query features.
- JSONB support for mixed relational/document patterns.
- Large ecosystem of tools, drivers, ORMs and operators.

---

## Weaknesses

- Requires schema and migration discipline.
- Not a cache or message broker.
- Horizontal write scaling is not as simple as adding more web pods.
- Running it in Kubernetes requires serious backup, storage and upgrade planning.

---

## Application Examples

- A Go API stores users, permissions and audit logs in PostgreSQL.
- A dashboard backend stores normalized cluster inventory and configuration.
- A service uses PostgreSQL transactions for workflows that must either fully succeed or fully roll back.
- A reporting endpoint uses SQL joins to combine users, nodes, services and events.
- JSONB columns are used for flexible metadata while keeping the rest of the schema relational.

---

## Alternatives

| Alternative | Notes |
|---|---|
| MySQL | Common and useful, especially for ecosystem compatibility |
| MariaDB | MySQL-compatible community option |
| SQLite | Excellent embedded database, not a shared cluster database |

---

## Comparison Notes

PostgreSQL is the safest default for custom services in this project. MySQL is valuable for compatibility and ecosystem learning. MongoDB is better when the data model is intentionally document-oriented. Redis is better for cache-like data, not durable relational state.

---

## Runtime Status

PostgreSQL is currently `⚫ Inactive` in all three shapes, and they arrive at different times:

1. **Identity instance on `pve0`** — first, because [Keycloak](../../security/rights-management/keycloak) is built before the cluster exists and the family apps launch with SSO rather than being migrated onto it later.
2. **Per-app databases** — with each family app, once the [ZFS pool](../../storage/zfs-nas) exists.
3. **Cluster instance** — after Longhorn, Vault and Velero, when the first custom service needs it.

It is also a consumer of [Home Assistant](../../../../applications/home-assistant)'s recorder requirement: SQLite does not enjoy being rescheduled across nodes.

---

## Operator Note

Evaluate CloudNativePG before hand-writing StatefulSets. Operators usually provide better backup, failover and maintenance workflows.

See also: [`operators`](../../../kubernetes/operators)

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/databases/postgresql/
```

---

## Learning Links

- [PostgreSQL documentation](https://www.postgresql.org/docs/)
- [Wikipedia: PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL)
- [Wikipedia: Relational database](https://en.wikipedia.org/wiki/Relational_database)
- [Wikipedia: ACID](https://en.wikipedia.org/wiki/ACID)
