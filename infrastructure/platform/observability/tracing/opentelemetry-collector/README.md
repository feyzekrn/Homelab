# OpenTelemetry Collector

[<- Back to Tracing](../README.md)

The OpenTelemetry Collector receives, processes and exports telemetry data such as traces, metrics and logs.

It is vendor-neutral and is becoming the standard integration layer for observability.

OpenTelemetry is a standard way for applications to emit telemetry. The Collector is the pipeline component that receives this telemetry, processes it and sends it to one or more backends.

For example, a Go API can send OTLP traces to the Collector. The Collector can batch those traces, add metadata and export them to Jaeger. Later, the backend can change without rewriting the application instrumentation.

The Collector is valuable because it decouples application code from observability products. Applications speak OpenTelemetry; the Collector handles routing and backend details.

---

## Why It Fits

OpenTelemetry lets custom services emit telemetry without coupling them directly to Jaeger, Zipkin, Prometheus or another backend.

For this homelab, that matters once custom services exist. It allows the project to learn modern instrumentation patterns while keeping backend choices flexible.

---

## Used For

- receiving OTLP traces from services
- exporting traces to Jaeger
- experimenting with metrics pipelines
- future vendor-neutral observability patterns
- adding resource metadata to telemetry
- batching and routing telemetry data

---

## Strengths

- Vendor-neutral standard with broad ecosystem support.
- Keeps application code less dependent on one backend.
- Can receive, process and export traces, metrics and logs.
- Good fit for modern distributed systems.
- Supports local development and Kubernetes deployment patterns.

---

## Weaknesses

- Adds another moving part before telemetry reaches a backend.
- Configuration can become complex if many pipelines are added.
- It does not store or visualize data by itself.
- Instrumentation still has to be added to applications.

---

## Runtime Status

OpenTelemetry Collector is currently `⚫ Inactive`. It is optional until custom services emit telemetry.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/infrastructure/platform/observability/tracing/opentelemetry-collector/
```

---

## Learning Links

- [OpenTelemetry Collector documentation](https://opentelemetry.io/docs/collector/)
- [OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/)
- [Wikipedia: Distributed tracing](https://en.wikipedia.org/wiki/Distributed_tracing)
