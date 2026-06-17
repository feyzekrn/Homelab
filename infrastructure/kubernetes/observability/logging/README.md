# Logging

[<- Back to Observability](../README.md)

Logs are event records emitted by applications and infrastructure components.

The goal is not just to store logs, but to make failures searchable and understandable.

---

## Components

| Component | Role | Documentation |
|---|---|---|
| Fluent Bit | Lightweight log collector on nodes | [fluent-bit](./fluent-bit) |
| OpenSearch | Search and analytics backend similar to Elasticsearch | [opensearch](./opensearch) |

---

## Recommended Direction

Use Fluent Bit for collection and OpenSearch for storage and search.

This is similar to an ELK-style setup, but avoids tying the project too early to a heavier Elasticsearch and Logstash deployment.
