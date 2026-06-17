# MongoDB

[<- Back to Databases](../README.md)

MongoDB is the document database for this homelab.

It is useful for JSON-heavy workloads, flexible schemas and services where document modeling is intentionally part of the experiment.

---

## Used For

- document-oriented application data
- JSON-heavy API experiments
- schema design comparison against relational models
- replica set and backup learning

---

## Application Examples

- A service stores flexible device metadata where different node types have different fields.
- A prototype API stores nested JSON documents without designing a strict relational schema first.
- An event viewer stores denormalized read models optimized for dashboard queries.
- A learning project compares MongoDB document modeling against PostgreSQL JSONB.

---

## Alternatives

| Alternative | Notes |
|---|---|
| PostgreSQL JSONB | Often enough for JSON data while keeping relational strength |
| CouchDB | Document database with replication focus |
| FerretDB | MongoDB-compatible layer backed by PostgreSQL |

---

## Comparison Notes

MongoDB is useful when document structure is the natural model. PostgreSQL JSONB may be enough when the application still benefits from relational integrity, joins and SQL. Redis is not a durable document database; it is better for cache and temporary state.

---

## Runtime Status

MongoDB is currently `⚫ Inactive`. It should run when document modeling or MongoDB-specific application support is part of the learning goal.

---

## Operator Note

Evaluate MongoDB Community Kubernetes Operator before building the deployment by hand.

See also: [`../../operators`](../../operators)

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/databases/mongodb/
```
