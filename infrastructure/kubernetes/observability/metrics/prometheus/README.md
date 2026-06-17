# Prometheus

[<- Back to Metrics](../README.md)

Prometheus collects and stores metrics from Kubernetes, nodes and applications.

It is the default metrics system in the Kubernetes ecosystem and the best first choice for this homelab.

---

## Used For

- node metrics
- Kubernetes control plane metrics
- pod and container metrics
- Longhorn metrics
- database exporter metrics
- alerting experiments

---

## Why It Fits

Prometheus teaches the standard Kubernetes observability model: scraping targets, labels, recording rules, alert rules and exporters.

---

## Alternatives

| Alternative | Notes |
|---|---|
| VictoriaMetrics | Strong long-term Prometheus-compatible storage |
| InfluxDB | Good for custom time-series data |
| Grafana Mimir | Scalable Prometheus-compatible backend, heavier |

---

## Runtime Status

Prometheus is currently `⚫ Inactive`. It is optional at the beginning, but should become part of the platform once databases and services run regularly.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/observability/prometheus/
```
