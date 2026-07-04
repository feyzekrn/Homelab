# MongoDB

[<- Back to Databases](../README.md)

MongoDB is the document database for this homelab.

It is useful for JSON-heavy workloads, flexible schemas and services where document modeling is intentionally part of the experiment.

MongoDB stores data as documents instead of rows in relational tables. A document is similar to a JSON object: it can contain nested fields, arrays and flexible structures.

This model can be useful when data naturally arrives as documents or when different records have different shapes. For example, hardware metadata for different device types may not fit cleanly into one strict table early in a prototype.

MongoDB is not a shortcut around data modeling. Document databases still need thoughtful schema design, indexes, backup planning and query discipline. The modeling question changes from "which tables and joins?" to "which document shape matches the access pattern?"

---

## Why It Fits

MongoDB is useful when document structure is the natural model or when MongoDB-specific application support is part of the learning goal.

It is also useful as a comparison against PostgreSQL JSONB. Many systems that look like they need MongoDB can be modeled well in PostgreSQL. This homelab should document the difference instead of choosing a document database by habit.

---

## Used For

- document-oriented application data
- JSON-heavy API experiments
- schema design comparison against relational models
- replica set and backup learning
- denormalized read-model experiments

---

## Strengths

- Natural fit for nested JSON-like records.
- Flexible document model for evolving prototypes.
- Large ecosystem and many application examples.
- Useful for learning replica sets and document indexing.

---

## Weaknesses

- Flexible schemas can turn into inconsistent data without discipline.
- Joins and relational integrity are not its strongest area.
- PostgreSQL JSONB may be enough for many mixed workloads.
- Running MongoDB reliably in Kubernetes still requires backups, storage and operator planning.

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

---

## Learning Links

- [MongoDB documentation](https://www.mongodb.com/docs/)
- [Wikipedia: MongoDB](https://en.wikipedia.org/wiki/MongoDB)
- [Wikipedia: Document-oriented database](https://en.wikipedia.org/wiki/Document-oriented_database)
- [Wikipedia: NoSQL](https://en.wikipedia.org/wiki/NoSQL)
