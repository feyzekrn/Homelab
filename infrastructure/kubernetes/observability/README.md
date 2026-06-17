# Observability

[<- Back to Kubernetes](../README.md)

Observability is how the cluster explains itself: metrics show what is happening, logs explain what happened and traces show how requests move through services.

---

## Areas

| Area | Purpose | Documentation |
|---|---|---|
| Metrics | Numeric time-series about systems and services | [metrics](./metrics) |
| Logging | Structured and searchable logs | [logging](./logging) |
| Tracing | Request flow across services | [tracing](./tracing) |

---

## Recommended Path

Start with metrics first, then logs, then tracing:

1. Prometheus and Grafana for infrastructure visibility.
2. Fluent Bit and OpenSearch for searchable logs.
3. OpenTelemetry Collector and Jaeger when custom services start communicating.

This order keeps the platform understandable while still moving toward a real production-style setup.
