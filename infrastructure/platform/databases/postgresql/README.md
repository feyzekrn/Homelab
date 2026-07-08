# PostgreSQL

[<- Back to Databases](../README.md)

PostgreSQL is the default relational database for this homelab.

It is mature, widely used, strict enough to teach good data modeling and flexible enough for most full-stack applications.

PostgreSQL stores data in tables with rows, columns, constraints, indexes and transactions. It is a relational database, which means it is strong at representing structured data and relationships between data.

For example, users can belong to groups, groups can have roles, roles can grant permissions and audit logs can reference the user who performed an action. SQL lets applications query and join that data reliably.

PostgreSQL also supports JSONB, full-text search, extensions and advanced indexing, so it can handle many workloads that might otherwise require a separate specialized database.

---

## Why It Fits

PostgreSQL is the best default choice for new services because it handles relational data, JSON fields, indexing, migrations and transactional workloads well.

It is also a good teaching database. It rewards clear schemas, constraints, migrations and backup discipline. Those habits transfer well to professional backend development.

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

PostgreSQL is currently `⚫ Inactive`. It should become one of the first databases to run once Longhorn, backups and basic monitoring are ready.

---

## Operator Note

Evaluate CloudNativePG before hand-writing StatefulSets. Operators usually provide better backup, failover and maintenance workflows.

See also: [`../../operators`](../../../kubernetes/operators)

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
