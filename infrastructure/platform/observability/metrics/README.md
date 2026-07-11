# Metrics

[<- Back to Observability](../README.md)

Metrics are numeric measurements collected over time.

They answer questions like: Is the node under CPU pressure? Is Longhorn healthy? Is PostgreSQL using too much memory? Are requests getting slower?

A metric is a number with labels and a timestamp. Examples include CPU usage, memory usage, request count, request latency, disk space, pod restart count and error rate. Because metrics are numbers over time, they are good for dashboards, alerts and capacity planning.

Metrics are not detailed stories. They usually tell you that something changed or broke, but not every reason why. A metric might show that API errors increased at 13:05. Logs and traces may then explain which error happened and which request path failed.

---

## Why This Matters

Metrics are the fastest way to understand the current health of the cluster. They turn resource usage, request rates, latency and error counts into time-series data that can be queried and visualized.

In a homelab, metrics help you learn how workloads behave under load and how much capacity the hardware really has. In companies, metrics are used for alerting, capacity planning, incident response and service-level tracking.

---

## What You Can Do With It

- monitor CPU, memory, disk and network usage
- track pod restarts and resource pressure
- build Grafana dashboards
- observe database and storage behavior
- create alerts for failures
- compare idle, normal and load-test scenarios

---

## Components

| Name | Path | Idle RAM | Role |
|---|---|---|---|
| Prometheus | [docs](./prometheus) · [chart](../../../../helm-charts/infrastructure/platform/observability/metrics/prometheus) · [config](./prometheus/terraform) | ~0.5–1 GB+ | Metrics collection and alerting |
| Grafana | [docs](./grafana) · [chart](../../../../helm-charts/infrastructure/platform/observability/metrics/grafana) · [config](./grafana/terraform) | ~0.15–0.3 GB | Dashboards and visualization |

---

## Baseline

Prometheus and Grafana are the standard starting point for Kubernetes metrics. They should be added when there are enough running services to justify monitoring.

---

## Learning Links

- [Wikipedia: Time series](https://en.wikipedia.org/wiki/Time_series)
- [Wikipedia: System monitoring](https://en.wikipedia.org/wiki/System_monitoring)
- [Prometheus documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana documentation](https://grafana.com/docs/)
