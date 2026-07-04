# Observability

[<- Back to Kubernetes](../README.md)

Observability is how the cluster explains itself: metrics show what is happening, logs explain what happened and traces show how requests move through services.

Observability is the ability to understand a running system from the signals it emits. In Kubernetes, the system is too dynamic to debug only by looking at one machine. Pods move, containers restart, Services route traffic, volumes attach and detach, and applications call each other.

The three core signal types are different:

- Metrics are numbers over time, such as CPU usage, request count or error rate.
- Logs are timestamped event records, such as startup messages, stack traces or audit entries.
- Traces show the path of one request across multiple services.

Good observability does not mean collecting everything forever. It means collecting the right signals so failures can be understood without guessing.

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

---

## Common Beginner Mistakes

- Installing dashboards before deciding which questions they should answer.
- Keeping every log forever without retention or storage planning.
- Adding tracing before there are multiple custom services to trace.
- Alerting on noisy symptoms instead of actionable failures.
- Treating observability as a replacement for backups, tests or clear architecture.

---

## Learning Links

- [Wikipedia: Observability](https://en.wikipedia.org/wiki/Observability_(software))
- [Wikipedia: System monitoring](https://en.wikipedia.org/wiki/System_monitoring)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [Prometheus documentation](https://prometheus.io/docs/)
- [Grafana documentation](https://grafana.com/docs/)
