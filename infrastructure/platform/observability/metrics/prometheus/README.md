# Prometheus

[<- Back to Metrics](../README.md)

Prometheus collects and stores metrics from Kubernetes, nodes and applications. It is the **chosen metrics stack** (`k8s`).

It runs on the cluster, but it is the one observability component that deliberately **looks beyond it**: `pve0`, the MikroTik switch and OPNsense are scrape targets too. Monitoring is the exception to the two-world separation — a dashboard that only shows half the homelab is not worth opening.

Prometheus is a time-series database and monitoring system. It regularly scrapes metrics from configured targets, stores those measurements and lets users query them with PromQL.

For example, Prometheus can scrape node metrics, Kubernetes control plane metrics, application metrics and database exporter metrics. Grafana can then visualize that data in dashboards. Alertmanager can route alerts when Prometheus rules detect a problem.

Prometheus is pull-based by default: it usually asks targets for metrics instead of waiting for targets to push data. That model is common in Kubernetes because services and pods can be discovered dynamically.

---

## Why It Fits

Prometheus teaches the standard Kubernetes observability model: scraping targets, labels, recording rules, alert rules and exporters.

It is also a practical foundation for the homelab. Before adding a logging stack or tracing backend, Prometheus can answer the most immediate operational questions about resource usage, restarts, saturation and service health.

---

## Prerequisites

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../../kubernetes/cilium) | It runs as pods |
| [Longhorn](../../../storage/longhorn) | Metric storage is persistent and grows continuously |
| A retention policy | Decided up front — the default fills a volume faster than expected |
| [Grafana](../grafana) | Prometheus has a query UI, not a dashboard |
| Network path into VLAN 30 | To scrape `pve0`, the switch and OPNsense across the zone boundary |

**Scraping across worlds needs a firewall rule.** The management zone is deliberately closed, so allowing the cluster to reach the exporters on `pve0`, the MikroTik and OPNsense is an explicit exception that has to be written into the OPNsense ruleset. Worth planning with the [network design](../../../../../setup/networking/design.md) rather than discovering as a broken dashboard.

---

## Used For

- node metrics
- Kubernetes control plane metrics
- pod and container metrics
- Longhorn metrics
- database exporter metrics
- alerting experiments
- service-level indicator experiments

---

## Strengths

- Kubernetes ecosystem standard for metrics.
- Strong service discovery and labeling model.
- PromQL is powerful for time-series queries.
- Works well with Grafana and Alertmanager.
- Many applications and operators expose Prometheus-compatible metrics.

---

## Weaknesses

- Long-term storage and high cardinality require planning.
- PromQL has a learning curve.
- It is not a log system and should not store arbitrary text events.
- Metrics labels can explode storage usage if used carelessly.
- Highly available production setups are more complex than a single instance.

---

## Alternatives

| Alternative | Notes |
|---|---|
| VictoriaMetrics | Strong long-term Prometheus-compatible storage |
| InfluxDB | Good for custom time-series data |
| Grafana Mimir | Scalable Prometheus-compatible backend, heavier |

---

## Runtime Status

Prometheus is currently `⚫ Inactive`. It is deployed together with [Grafana](../grafana), after storage works and before there are many services — early enough that the baseline of "normal" is recorded before anything is tuned.

It is also a prerequisite for two later components: [Loki](../../logging/loki) shares its dashboard, and [Argo Rollouts](../../../../kubernetes/gitops/argo-rollouts) cannot gate a canary release without metrics to gate on.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/infrastructure/platform/observability/metrics/prometheus/
```

---

## Learning Links

- [Prometheus documentation](https://prometheus.io/docs/introduction/overview/)
- [Prometheus Operator documentation](https://prometheus-operator.dev/)
- [Wikipedia: Prometheus](https://en.wikipedia.org/wiki/Prometheus_(software))
- [Wikipedia: Time series database](https://en.wikipedia.org/wiki/Time_series_database)
