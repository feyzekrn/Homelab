# Grafana

[<- Back to Metrics](../README.md)

Grafana is the dashboard layer for metrics, logs and traces.

It does not collect data by itself. It visualizes data from systems such as Prometheus, Loki, Jaeger or InfluxDB.

In this homelab it is the **single pane for everything**: [Prometheus](../prometheus) metrics, [Loki](../../logging/loki) logs and [Jaeger](../../tracing/jaeger) traces all land here — including the metrics scraped from `pve0`, the switch and OPNsense. It is the one place where both worlds appear together.

Grafana is the visual interface for observability data. It connects to data sources, runs queries and displays results as dashboards, graphs, tables, gauges and alerts.

For example, Prometheus may store CPU metrics, Loki may store logs and Jaeger may store traces. Grafana provides a single UI that links those signals together. It is usually the first observability tool a human opens during troubleshooting.

---

## Prerequisites

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../../kubernetes/cilium) | It runs as pods |
| At least one data source | [Prometheus](../prometheus) first — Grafana displays nothing on its own |
| [Longhorn](../../../storage/longhorn) | Dashboards, users and settings are state worth keeping |
| [Traefik](../../../ingress/traefik) + [cert-manager](../../../ingress/cert-manager) | It is a web UI and needs a hostname |
| [Keycloak](../../../security/rights-management/keycloak) | Optional — OIDC login instead of a local admin account |

Deploy Prometheus first. Grafana without a data source is an empty dashboard that teaches nothing.

Grafana is not a replacement for the data sources behind it. If Prometheus is not collecting metrics, Grafana has no Prometheus metrics to show.

---

## Used For

- Kubernetes dashboards
- node resource dashboards
- database dashboards
- power and temperature dashboards
- service health views
- linking metrics, logs and traces

---

## Strengths

- Excellent dashboard and visualization ecosystem.
- Supports many data sources.
- Common in Kubernetes and infrastructure monitoring.
- Useful for both technical debugging and high-level status pages.
- Can integrate with SSO providers such as Keycloak.

---

## Weaknesses

- Dashboards can become decorative if they do not answer operational questions.
- It depends on correctly configured data sources.
- Permissions and public sharing must be configured carefully.
- Too many dashboards can make failures harder, not easier, to understand.

---

## Runtime Status

Grafana is currently `⚫ Inactive`. It is optional early, but becomes useful as soon as Prometheus or another data source exists.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/infrastructure/platform/observability/metrics/grafana/
```

---

## Learning Links

- [Grafana documentation](https://grafana.com/docs/grafana/latest/)
- [Wikipedia: Grafana](https://en.wikipedia.org/wiki/Grafana)
- [Wikipedia: Data visualization](https://en.wikipedia.org/wiki/Data_and_information_visualization)
