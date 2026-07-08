# Grafana

[<- Back to Metrics](../README.md)

Grafana is the dashboard layer for metrics, logs and traces.

It does not collect data by itself. It visualizes data from systems such as Prometheus, OpenSearch, Loki, Jaeger or InfluxDB.

Grafana is the visual interface for observability data. It connects to data sources, runs queries and displays results as dashboards, graphs, tables, gauges and alerts.

For example, Prometheus may store CPU metrics, OpenSearch may store logs and Jaeger may store traces. Grafana can provide a single UI that links those signals together. It is usually the first observability tool a human opens during troubleshooting.

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
