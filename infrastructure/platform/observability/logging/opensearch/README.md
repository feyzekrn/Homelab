# OpenSearch

[<- Back to Logging](../README.md)

OpenSearch is a search and analytics engine derived from Elasticsearch.

In this homelab, OpenSearch is the **documented alternative** to [Loki](../loki), which is the chosen logging backend. It is not planned for deployment.

OpenSearch stores documents and makes them searchable. In a logging stack, each log event becomes a document. Users can search by message, timestamp, namespace, pod name, severity or other fields.

---

## Why It Lost

The deciding factor is the cost of full-text indexing, and it is not a close call at this scale:

| | OpenSearch | [Loki](../loki) |
|---|---|---|
| Idle RAM | ~2–4 GB+ | ~0.2–0.4 GB |
| Indexes | Every field of every log line | Labels only |
| Dashboard | OpenSearch Dashboards, a second UI to operate | [Grafana](../../metrics/grafana), already running |

Roughly 3 GB of RAM before a single log line is stored is comparable to the *entire rest* of the observability stack — on nodes with 8–16 GB each, that is capacity taken directly from the workloads the cluster exists to run.

What is genuinely given up: real full-text search across large log corpora, richer aggregation and analytics, and the ELK-family skills that are common in industry. Those are real losses. They are accepted because the questions actually asked here — "what did this pod do around this spike" — are the ones Loki is built for, and the honest answer is that a homelab does not generate a corpus worth indexing.

---

## When It Would Be The Right Choice

Not a hypothetical, so the trigger is worth naming: OpenSearch becomes correct when logs stop being a debugging aid and become **data**. Security event analysis, long-retention audit trails, or anything requiring aggregation across millions of events by arbitrary fields. If this homelab ever grows a real log-analytics goal, this is the page to come back to — and by then the cluster will likely have the RAM to afford it.

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

OpenSearch is `⚫ Inactive` and **not planned**. [Loki](../loki) is the chosen logging backend; this page exists for comparison and as the documented upgrade path if log analytics ever becomes a real requirement.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/infrastructure/platform/observability/logging/opensearch/
```

---

## Learning Links

- [OpenSearch documentation](https://opensearch.org/docs/)
- [Wikipedia: OpenSearch](https://en.wikipedia.org/wiki/OpenSearch_(software))
- [Wikipedia: Elasticsearch](https://en.wikipedia.org/wiki/Elasticsearch)
- [Wikipedia: Full-text search](https://en.wikipedia.org/wiki/Full-text_search)
