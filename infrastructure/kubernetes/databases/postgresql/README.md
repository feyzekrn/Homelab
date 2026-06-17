# PostgreSQL

[<- Back to Databases](../README.md)

PostgreSQL is the default relational database for this homelab.

It is mature, widely used, strict enough to teach good data modeling and flexible enough for most full-stack applications.

---

## Why It Fits

PostgreSQL is the best default choice for new services because it handles relational data, JSON fields, indexing, migrations and transactional workloads well.

---

## Used For

- primary application databases
- admin dashboard backend data
- relational modeling practice
- migration tooling practice
- backup and restore testing

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

PostgreSQL is currently `⚫ Inactive`. It should become one of the first databases to run once Longhorn, backups and basic monitoring are ready.

---

## Operator Note

Evaluate CloudNativePG before hand-writing StatefulSets. Operators usually provide better backup, failover and maintenance workflows.

See also: [`../../operators`](../../operators)

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/databases/postgresql/
```
