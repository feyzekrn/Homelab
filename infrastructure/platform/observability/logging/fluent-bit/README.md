# Fluent Bit

[<- Back to Logging](../README.md)

Fluent Bit is a lightweight log collector commonly deployed as a DaemonSet on Kubernetes nodes.

It tails container logs, enriches them with Kubernetes metadata and forwards them to a backend such as OpenSearch.

In Kubernetes, each node writes container logs locally. Fluent Bit runs on every node, reads those logs, adds useful metadata such as namespace, pod name and container name, optionally filters or parses the records and forwards them to a log backend.

The DaemonSet model is important: one Fluent Bit pod runs per node, so every node has a local collector. This avoids requiring every application to know where the logging backend is.

---

## Why It Fits

Fluent Bit is smaller and simpler than Logstash for node-level log collection. It is a good first collector for a homelab.

It also teaches the normal logging pipeline shape: collect, enrich, filter, buffer and forward. Those ideas apply whether the final backend is OpenSearch, Loki, ClickHouse or a managed logging service.

---

## Used For

- collecting container logs
- adding Kubernetes metadata
- forwarding logs to OpenSearch
- filtering noisy logs
- learning log parsing and routing pipelines

---

## Strengths

- Lightweight enough for small clusters.
- Designed for log collection and forwarding.
- Common Kubernetes DaemonSet deployment model.
- Supports many outputs and parsers.
- Less resource-heavy than Logstash.

---

## Weaknesses

- It is a collector, not a search backend.
- Parsing and multiline log handling need careful configuration.
- Bad filters can drop important debugging data.
- Backpressure behavior should be understood before relying on it for critical logs.

---

## Alternatives

| Alternative | Notes |
|---|---|
| Logstash | Powerful processing pipeline, heavier to operate |
| Vector | Modern and fast observability pipeline |
| Promtail | Best paired with Loki |

---

## Runtime Status

Fluent Bit is currently `⚫ Inactive`. It is optional until a logging backend exists.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/infrastructure/platform/observability/logging/fluent-bit/
```

---

## Learning Links

- [Fluent Bit documentation](https://docs.fluentbit.io/)
- [Wikipedia: Log file](https://en.wikipedia.org/wiki/Log_file)
- [Kubernetes logging architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
