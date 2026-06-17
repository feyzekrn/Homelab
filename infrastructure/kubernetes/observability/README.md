# Observability

[<- Back to Kubernetes](../README.md)

Observability is how the cluster explains itself: metrics show what is happening, logs explain what happened and traces show how requests move through services.

---

## Why This Matters

Without observability, debugging becomes guesswork. Kubernetes adds many moving parts: nodes, pods, services, volumes, ingress, databases and custom applications. Metrics, logs and traces are the tools that make those parts inspectable.

In a homelab, observability helps answer basic operational questions: Is the node overloaded? Why did a pod restart? Is storage slow? Did an API request fail in the frontend, backend or database?

In companies, observability supports incident response, service-level objectives, capacity planning, security investigations and product debugging. The homelab version should teach the same mental model without immediately copying a large enterprise stack.

---

## What You Can Do With It

- monitor nodes and pods
- build Grafana dashboards
- search application and platform logs
- trace requests across services
- alert on unhealthy components
- compare resource usage before and after changes
- understand failures instead of only restarting pods

---

## Areas

| Path | Purpose |
|---|---|
| [`./metrics`](./metrics) | Numeric time-series about systems and services |
| [`./logging`](./logging) | Structured and searchable logs |
| [`./tracing`](./tracing) | Request flow across services |

---

## Recommended Path

Start with metrics first, then logs, then tracing:

1. Prometheus and Grafana for infrastructure visibility.
2. Fluent Bit and OpenSearch for searchable logs.
3. OpenTelemetry Collector and Jaeger when custom services start communicating.

This order keeps the platform understandable while still moving toward a real production-style setup.
