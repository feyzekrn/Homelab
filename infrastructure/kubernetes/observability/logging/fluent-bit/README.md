# Fluent Bit

[<- Back to Logging](../README.md)

Fluent Bit is a lightweight log collector commonly deployed as a DaemonSet on Kubernetes nodes.

It tails container logs, enriches them with Kubernetes metadata and forwards them to a backend such as OpenSearch.

---

## Why It Fits

Fluent Bit is smaller and simpler than Logstash for node-level log collection. It is a good first collector for a homelab.

---

## Used For

- collecting container logs
- adding Kubernetes metadata
- forwarding logs to OpenSearch
- filtering noisy logs

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
../../../../../helm-charts/observability/fluent-bit/
```
