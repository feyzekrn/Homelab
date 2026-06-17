# Tracing

[<- Back to Observability](../README.md)

Distributed tracing shows how a request moves through multiple services.

Tracing becomes valuable once there are custom services calling each other. Before that, metrics and logs usually provide more immediate value.

---

## Components

| Component | Role | Documentation |
|---|---|---|
| OpenTelemetry Collector | Vendor-neutral telemetry pipeline | [opentelemetry-collector](./opentelemetry-collector) |
| Jaeger | Trace storage and UI | [jaeger](./jaeger) |
| Zipkin | Simpler tracing backend and compatibility target | [zipkin](./zipkin) |

---

## Recommended Direction

Use OpenTelemetry as the instrumentation and collection standard. Use Jaeger as the first trace backend. Keep Zipkin documented for compatibility and comparison.
