# OpenSearch

[<- Back to Logging](../README.md)

OpenSearch is a search and analytics engine derived from Elasticsearch.

In this homelab, it is the preferred ELK-style logging backend candidate.

OpenSearch stores documents and makes them searchable. In a logging stack, each log event becomes a document. Users can search by message, timestamp, namespace, pod name, severity or other fields.

OpenSearch is useful when logs need full-text search, filtering, dashboards and retention policies. It is heavier than simply viewing `kubectl logs`, but it gives a much more powerful troubleshooting workflow once many services exist.

---

## Why It Fits

An ELK-style stack teaches useful production concepts: indexing, retention, log search, dashboards and resource planning. OpenSearch keeps that learning path available while staying aligned with an open-source-friendly stack.

This does not mean OpenSearch should run from day one. It consumes CPU, memory and storage. It should be installed when searchable log retention is an actual learning goal or operational need.

---

## Used For

- storing Kubernetes logs
- searching application logs
- investigating incidents
- learning index lifecycle and retention
- experimenting with log analytics

---

## Strengths

- Powerful search and analytics model.
- Good fit for structured and semi-structured logs.
- Teaches indexing, retention and query concepts used in larger platforms.
- OpenSearch Dashboards can provide log exploration and visualization.

---

## Weaknesses

- Resource-heavy for a small homelab.
- Index lifecycle and retention require planning.
- Storage usage can grow quickly with noisy logs.
- Operating a search cluster is more complex than using a lightweight log backend.

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

---

## Learning Links

- [OpenSearch documentation](https://opensearch.org/docs/)
- [Wikipedia: OpenSearch](https://en.wikipedia.org/wiki/OpenSearch_(software))
- [Wikipedia: Elasticsearch](https://en.wikipedia.org/wiki/Elasticsearch)
- [Wikipedia: Full-text search](https://en.wikipedia.org/wiki/Full-text_search)
