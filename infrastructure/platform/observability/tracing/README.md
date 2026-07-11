# Tracing

[<- Back to Observability](../README.md)

Distributed tracing shows how a request moves through multiple services.

Tracing becomes valuable once there are custom services calling each other. Before that, metrics and logs usually provide more immediate value.

A trace follows one request as it travels through a distributed system. If a dashboard calls an API, the API calls another service and that service queries a database, a trace can show each step as a span with timing information.

This is different from logs. Logs are local event records. A trace connects related work across service boundaries. That connection depends on context propagation: services pass trace identifiers along when they call each other.

Tracing is most useful after the project has multiple custom services. A single monolithic app or a mostly platform-only cluster will not benefit as much.

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

| Name | Path | Idle RAM | Role |
|---|---|---|---|
| OpenTelemetry Collector | [docs](./opentelemetry-collector) · [chart](../../../../helm-charts/infrastructure/platform/observability/tracing/opentelemetry-collector) · [config](./opentelemetry-collector/terraform) | ~0.1–0.2 GB | Vendor-neutral telemetry pipeline |
| Jaeger | [docs](./jaeger) · [chart](../../../../helm-charts/infrastructure/platform/observability/tracing/jaeger) · [config](./jaeger/terraform) | ~0.2–0.5 GB | Trace storage and UI |
| Zipkin | [docs](./zipkin) · [chart](../../../../helm-charts/infrastructure/platform/observability/tracing/zipkin) · [config](./zipkin/terraform) | ~0.3–0.5 GB | Simpler tracing backend and compatibility target |

---

## Recommended Direction

Use OpenTelemetry as the instrumentation and collection standard. Use Jaeger as the first trace backend. Keep Zipkin documented for compatibility and comparison.

---

## Learning Links

- [Wikipedia: Distributed tracing](https://en.wikipedia.org/wiki/Distributed_tracing)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [Jaeger documentation](https://www.jaegertracing.io/docs/)
- [Zipkin documentation](https://zipkin.io/pages/documentation.html)
