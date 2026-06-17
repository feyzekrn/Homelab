# Metrics

[<- Back to Observability](../README.md)

Metrics are numeric measurements collected over time.

They answer questions like: Is the node under CPU pressure? Is Longhorn healthy? Is PostgreSQL using too much memory? Are requests getting slower?

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

| Path | Role |
|---|---|
| [`./prometheus`](./prometheus) | Metrics collection and alerting |
| [`./grafana`](./grafana) | Dashboards and visualization |

---

## Baseline

Prometheus and Grafana are the standard starting point for Kubernetes metrics. They should be added when there are enough running services to justify monitoring.
