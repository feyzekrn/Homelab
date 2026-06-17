# OpenSearch

[<- Back to Logging](../README.md)

OpenSearch is a search and analytics engine derived from Elasticsearch.

In this homelab, it is the preferred ELK-style logging backend candidate.

---

## Why It Fits

An ELK-style stack teaches useful production concepts: indexing, retention, log search, dashboards and resource planning. OpenSearch keeps that learning path available while staying aligned with an open-source-friendly stack.

---

## Used For

- storing Kubernetes logs
- searching application logs
- investigating incidents
- learning index lifecycle and retention

---

## Alternatives

| Alternative | Notes |
|---|---|
| Elasticsearch + Logstash + Kibana | Classic ELK stack, licensing and weight should be considered |
| Loki | Very strong Kubernetes logging option, cheaper to run |
| ClickHouse | Excellent analytics backend, more custom setup |

---

## Runtime Status

OpenSearch is currently `⚫ Inactive`. It can be resource-heavy, so run it when there is a real logging goal.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/observability/opensearch/
```
