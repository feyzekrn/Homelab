# Loki

[<- Back to Logging](../README.md)

Loki is a log aggregation system from the Grafana project, and the **chosen logging backend** for this homelab (`k8s`).

Its design goal is stated in its own tagline: *like Prometheus, but for logs*. Where a classic ELK-style stack indexes the full text of every log line, Loki indexes only a small set of **labels** — namespace, pod, container, node — and stores the log content itself compressed and unindexed. Queries then filter by label first and grep the matching chunks second.

That single decision is why it fits here. Full-text indexing is what makes [OpenSearch](../opensearch) need several gigabytes of RAM before storing a single line; skipping it brings the same practical capability down to a few hundred megabytes.

---

## Why It Is Chosen

| | Loki | [OpenSearch](../opensearch) |
|---|---|---|
| Idle RAM | ~0.2–0.4 GB | ~2–4 GB+ |
| Index | Labels only | Full text |
| Query language | LogQL — deliberately close to PromQL | Lucene / DSL |
| Dashboard | [Grafana](../../metrics/grafana), already deployed | Needs OpenSearch Dashboards |
| Best at | "Show me this pod's logs around this spike" | Analytics and search across large corpora |

Three reasons decide it:

**It costs what a homelab can pay.** OpenSearch's footprint is comparable to the entire rest of the observability stack. On three nodes with 8–16 GB each, that is capacity taken from the workloads the cluster exists to run.

**It shares Grafana with the metrics.** [Prometheus](../../metrics/prometheus) and Loki are queried from the same dashboard, with deliberately similar query languages. A latency spike on a graph and the log lines behind it end up one click apart, which is the actual reason to run logging at all.

**The queries match the need.** Homelab log questions are almost always "what did this component do just now" — scoped by pod and time. That is exactly the shape Loki optimises for. Full-text search across months of logs is a real capability, and one this project does not have a use for.

---

## Prerequisites

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../../kubernetes/cilium) | It runs as pods |
| [Longhorn](../../../storage/longhorn) | Persistent volume for the log chunks |
| [Grafana](../../metrics/grafana) | Loki has no UI of its own — Grafana *is* the interface |
| [Fluent Bit](../fluent-bit) | The collector that ships node and container logs into it |
| A retention policy | Decided before deploying, not after the volume fills |

Loki and [Fluent Bit](../fluent-bit) are two halves of one system: Fluent Bit tails the logs on every node and pushes them, Loki stores and serves them. Neither is useful alone.

---

## Used For

- reading container logs without `kubectl logs` and without guessing which pod
- correlating a metrics spike with what the application was doing at that moment
- keeping logs after a pod is gone — the case where `kubectl logs` fails entirely
- learning LogQL, which transfers directly to PromQL and back

---

## Strengths

- Very small footprint for what it delivers.
- Native Grafana integration; no second dashboard system.
- Label model is the same mental model as Prometheus.
- Object storage backend is supported, so [MinIO](../../../storage/minio) can hold the chunks.
- Simple to operate compared with any Elasticsearch-derived stack.

---

## Weaknesses

- Not a search engine. Broad full-text queries across everything are slow by design.
- Bad label choices cause cardinality explosions — the same trap Prometheus has.
- Retention and compaction need attention or the volume grows until it stops.
- Alerting on log content is possible but less mature than metric alerting.

---

## Runtime Status

Loki is `⚫ Inactive`. It is deployed after [Prometheus](../../metrics/prometheus) and [Grafana](../../metrics/grafana), because it is only useful once there is a dashboard to read it in and something running worth reading about.

The first candidate to point it at is whatever is failing most often at that moment — which in a fresh cluster is usually ingress and storage.

---

## Documentation

- [Loki documentation](https://grafana.com/docs/loki/latest/)
- [LogQL reference](https://grafana.com/docs/loki/latest/query/)
- [Loki GitHub](https://github.com/grafana/loki)
- [Wikipedia: Log management](https://en.wikipedia.org/wiki/Log_management)
