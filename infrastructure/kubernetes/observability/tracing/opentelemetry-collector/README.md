# OpenTelemetry Collector

[<- Back to Tracing](../README.md)

The OpenTelemetry Collector receives, processes and exports telemetry data such as traces, metrics and logs.

It is vendor-neutral and is becoming the standard integration layer for observability.

---

## Why It Fits

OpenTelemetry lets custom services emit telemetry without coupling them directly to Jaeger, Zipkin, Prometheus or another backend.

---

## Used For

- receiving OTLP traces from services
- exporting traces to Jaeger
- experimenting with metrics pipelines
- future vendor-neutral observability patterns

---

## Runtime Status

OpenTelemetry Collector is currently `⚫ Inactive`. It is optional until custom services emit telemetry.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/observability/opentelemetry-collector/
```
