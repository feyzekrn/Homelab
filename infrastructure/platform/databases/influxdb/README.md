# InfluxDB

[<- Back to Databases](../README.md)

InfluxDB is the optional time-series database for this homelab.

It is designed for timestamped measurements such as sensor data, power usage, temperature readings and custom hardware metrics.

A time-series database stores measurements indexed by time. Instead of asking "what is this user's email address?", a time-series query asks questions like "what was node temperature every minute for the last 24 hours?" or "how did power usage change over a week?"

InfluxDB is built for this kind of data. Each point has a timestamp, measurement values and tags that describe the source. That makes it useful for sensors, hardware monitoring and long-running measurements.

This overlaps with Prometheus, but the intent is different. Prometheus is the default for operational metrics and alerting. InfluxDB can be useful when custom measurements are application data, not just infrastructure health signals.

---

## Why It Fits

Prometheus is excellent for infrastructure metrics, but it is not always the best place for arbitrary long-term application or hardware measurements. InfluxDB is useful when the project needs queryable time-series data outside the Prometheus operational model.

For this homelab, that may include power usage, room temperature, fan behavior, hardware experiments or custom automation history.

---

## Used For

- power usage measurements
- temperature data
- hardware automation history
- custom sensor metrics
- experiments with time-series data modeling
- Grafana dashboards for long-term measurement trends

---

## Strengths

- Purpose-built for timestamped measurement data.
- Good fit for sensor and hardware histories.
- Integrates well with Grafana.
- Easier mental model for custom measurements than forcing everything into logs.

---

## Weaknesses

- Optional and specialized; not needed for most application state.
- Prometheus already covers many infrastructure metric needs.
- Retention and downsampling should be planned for long-running measurements.
- Query language and data model differ from SQL databases.

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
../../../../helm-charts/infrastructure/platform/databases/influxdb/
```

---

## Learning Links

- [InfluxDB documentation](https://docs.influxdata.com/influxdb/)
- [Wikipedia: InfluxDB](https://en.wikipedia.org/wiki/InfluxDB)
- [Wikipedia: Time series database](https://en.wikipedia.org/wiki/Time_series_database)
- [Wikipedia: Sensor](https://en.wikipedia.org/wiki/Sensor)
