# InfluxDB

[<- Back to Databases](../README.md)

InfluxDB is the optional time-series database for this homelab.

It is designed for timestamped measurements such as sensor data, power usage, temperature readings and custom hardware metrics.

---

## Why It Fits

Prometheus is excellent for infrastructure metrics, but it is not always the best place for arbitrary long-term application or hardware measurements. InfluxDB is useful when the project needs queryable time-series data outside the Prometheus operational model.

---

## Used For

- power usage measurements
- temperature data
- hardware automation history
- custom sensor metrics
- experiments with time-series data modeling

---

## Application Examples

- Store wattage measurements from the homelab power supply over time.
- Track node temperature, fan behavior or room temperature readings.
- Keep long-term hardware automation history separate from Prometheus.
- Build Grafana dashboards for custom sensor data.

---

## Alternatives

| Alternative | Notes |
|---|---|
| Prometheus | Best for infrastructure and service metrics |
| VictoriaMetrics | Strong Prometheus-compatible long-term metrics storage |
| TimescaleDB | PostgreSQL-based time-series extension |

---

## Comparison Notes

Prometheus is the default for infrastructure metrics and alerting. InfluxDB is better when custom timestamped measurements are treated as application data. TimescaleDB is useful when SQL access and relational joins are important for time-series data.

---

## Runtime Status

InfluxDB is currently `⚫ Inactive` and should run when a workload needs dedicated time-series storage.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/databases/influxdb/
```
