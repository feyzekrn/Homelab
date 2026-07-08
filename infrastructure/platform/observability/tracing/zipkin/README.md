# Zipkin

[<- Back to Tracing](../README.md)

Zipkin is a distributed tracing system focused on collecting and visualizing timing data for service calls.

It is simpler than many modern tracing stacks and remains useful as a compatibility target.

Zipkin records timing data for requests that pass through multiple services. It can show which service handled which part of a request and how long each part took.

Zipkin is older and simpler than many current OpenTelemetry-first setups, but many frameworks and examples still support Zipkin-style tracing. That makes it useful to understand even if it is not the primary recommendation for this project.

---

## Why It Is Documented

Zipkin is not the primary recommendation here. It is documented because many examples, frameworks and older systems still support Zipkin-style tracing.

It also gives a simpler comparison point against Jaeger and OpenTelemetry Collector. If a workload or tutorial emits Zipkin-compatible traces, the project should know where that fits.

---

## Strengths

- Simple tracing backend and UI.
- Long history in distributed tracing examples.
- Supported by many older frameworks and tutorials.
- Useful for compatibility testing.

---

## Weaknesses

- Not the primary modern standard for this project.
- Less flexible as a general telemetry pipeline than OpenTelemetry Collector.
- Should not be added unless compatibility or comparison is the goal.

---

## Runtime Status

Zipkin is currently `⚫ Inactive` and research-only for now. Prefer OpenTelemetry Collector plus Jaeger unless a workload specifically benefits from Zipkin.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/infrastructure/platform/observability/tracing/zipkin/
```

---

## Learning Links

- [Zipkin documentation](https://zipkin.io/pages/documentation.html)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [Wikipedia: Distributed tracing](https://en.wikipedia.org/wiki/Distributed_tracing)
