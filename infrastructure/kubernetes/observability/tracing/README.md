# Tracing

[<- Back to Observability](../README.md)

Distributed tracing shows how a request moves through multiple services.

Tracing becomes valuable once there are custom services calling each other. Before that, metrics and logs usually provide more immediate value.

---

## Why This Matters

When a request touches several services, logs from one process are not enough. Tracing connects the path: frontend, API, worker, database call and downstream service. It shows where time is spent and where failures happen.

In a homelab, tracing is mainly useful after custom services exist. In companies, tracing is important for microservices, distributed systems and performance debugging.

---

## What You Can Do With It

- follow one request across multiple services
- find slow dependencies
- compare latency before and after changes
- debug service-to-service failures
- learn OpenTelemetry instrumentation
- connect traces to metrics and logs later

---

## Components

| Path | Role |
|---|---|
| [`./opentelemetry-collector`](./opentelemetry-collector) | Vendor-neutral telemetry pipeline |
| [`./jaeger`](./jaeger) | Trace storage and UI |
| [`./zipkin`](./zipkin) | Simpler tracing backend and compatibility target |

---

## Recommended Direction

Use OpenTelemetry as the instrumentation and collection standard. Use Jaeger as the first trace backend. Keep Zipkin documented for compatibility and comparison.
