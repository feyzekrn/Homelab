# Jaeger

[<- Back to Tracing](../README.md)

Jaeger is a distributed tracing backend and UI.

It helps visualize request paths, latency and service dependencies.

Jaeger stores and displays traces. A trace is made of spans, and each span represents one unit of work such as an HTTP request, database call or message handler. Jaeger lets a user search traces, open a trace timeline and see where time was spent.

For example, if a dashboard action feels slow, Jaeger can show whether the delay happened in the frontend request, the API, an internal service call or a database query.

Jaeger is not the instrumentation standard by itself. In a modern setup, applications usually emit OpenTelemetry data, the OpenTelemetry Collector receives it and Jaeger stores or displays the trace data.

---

## Why It Fits

Jaeger is a strong first tracing backend because it is common, understandable and integrates well with OpenTelemetry.

It gives the homelab a concrete UI for learning spans, traces, context propagation and service latency. That makes tracing easier to understand than reading protocol documentation alone.

---

## Used For

- viewing request traces
- debugging service latency
- understanding distributed service calls
- learning trace spans and context propagation
- comparing service dependencies after architecture changes

---

## Strengths

- Clear UI for inspecting individual traces.
- Common distributed tracing backend.
- Works well with OpenTelemetry pipelines.
- Good learning tool for span structure and latency breakdowns.

---

## Weaknesses

- Useful only when applications are instrumented.
- Storage and retention need planning if trace volume grows.
- It is not a full metrics or logging platform.
- A single backend can become limiting in larger production architectures.

---

## Alternatives

| Alternative | Notes |
|---|---|
| Zipkin | Simpler tracing backend |
| Grafana Tempo | Strong Grafana ecosystem integration |
| OpenSearch tracing | Possible if OpenSearch stack is already running |

---

## Runtime Status

Jaeger is currently `⚫ Inactive`. It is optional until there are instrumented services.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/infrastructure/platform/observability/tracing/jaeger/
```

---

## Learning Links

- [Jaeger documentation](https://www.jaegertracing.io/docs/)
- [OpenTelemetry tracing documentation](https://opentelemetry.io/docs/concepts/signals/traces/)
- [Wikipedia: Distributed tracing](https://en.wikipedia.org/wiki/Distributed_tracing)
