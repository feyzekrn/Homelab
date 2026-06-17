# Metrics

[<- Back to Observability](../README.md)

Metrics are numeric measurements collected over time.

They answer questions like: Is the node under CPU pressure? Is Longhorn healthy? Is PostgreSQL using too much memory? Are requests getting slower?

---

## Components

| Component | Role | Documentation |
|---|---|---|
| Prometheus | Metrics collection and alerting | [prometheus](./prometheus) |
| Grafana | Dashboards and visualization | [grafana](./grafana) |

---

## Baseline

Prometheus and Grafana are the standard starting point for Kubernetes metrics. They should be added when there are enough running services to justify monitoring.
