# Logging

[<- Back to Observability](../README.md)

Logs are event records emitted by applications and infrastructure components.

The goal is not just to store logs, but to make failures searchable and understandable.

A log is a timestamped statement from a system. It might say that an application started, a user logged in, a database connection failed or a request returned an error. In Kubernetes, logs are produced by containers, nodes, control plane components and platform services.

`kubectl logs` is enough for one pod. It becomes weak when pods restart, disappear, scale horizontally or fail across multiple namespaces. A logging stack collects logs centrally, attaches Kubernetes metadata and makes them searchable after the original pod is gone.

Logs are different from metrics. Metrics show trends and health. Logs explain specific events. A useful platform needs both once the number of services grows.

---

## Why This Matters

Metrics tell you that something is wrong. Logs often explain what happened. A useful logging stack collects logs from pods and nodes, attaches Kubernetes metadata and makes the result searchable.

In a homelab, logging is useful once there are enough services that `kubectl logs` becomes annoying. In companies, log systems support debugging, audit trails, incident analysis and security investigations.

---

## What You Can Do With It

- collect logs from all pods
- search errors across namespaces
- attach namespace, pod and container metadata
- retain logs after pods are deleted
- investigate incidents after they happened
- compare lightweight collectors with heavier ELK-style stacks

---

## Components

| Name | Path | Status | Runs on | Idle RAM | Recommendation | Role |
|---|---|---|---|---|---|---|
| Fluent Bit | [docs](./fluent-bit) · [chart](../../../../helm-charts/infrastructure/platform/observability/logging/fluent-bit) · [config](./fluent-bit/terraform) | ⚫ Inactive | k8s | ~30–50 MB / node | Chosen collector | Lightweight log collector on nodes |
| Loki | [docs](./loki) · [chart](../../../../helm-charts/infrastructure/platform/observability/logging/loki) · [config](./loki/terraform) | ⚫ Inactive | k8s | ~0.2–0.4 GB | Chosen backend | Label-indexed log store, queried through Grafana |
| OpenSearch | [docs](./opensearch) | ⚫ Inactive | — | ~2–4 GB+ | Documented alternative | Search and analytics backend similar to Elasticsearch |

**Two halves of one system.** Fluent Bit tails logs on every node and pushes them; [Loki](./loki) stores and serves them. Neither is useful alone, and Loki has to exist before Fluent Bit is deployed — a collector with no reachable backend fills its buffer and silently drops.

---

## Recommended Direction

**Fluent Bit collects, Loki stores, [Grafana](../metrics/grafana) displays.**

The decision that shapes this stack is what gets indexed. [OpenSearch](./opensearch) indexes the full text of every log line, which is what makes it powerful and what makes it cost 2–4 GB of RAM before storing anything. Loki indexes only labels — namespace, pod, container — and greps the rest on demand, bringing the same practical capability down to a few hundred megabytes.

At homelab scale that trade is one-sided. The questions actually asked here are "what did this pod do around this spike", scoped by pod and time, which is exactly Loki's shape. Full-text search across months of logs is a real capability this project has no use for — and Loki shares the Grafana that already exists for metrics, so a latency graph and the log lines behind it end up one click apart.

---

## Learning Links

- [Wikipedia: Logging](https://en.wikipedia.org/wiki/Logging_(computing))
- [Wikipedia: Elasticsearch](https://en.wikipedia.org/wiki/Elasticsearch)
- [OpenSearch documentation](https://opensearch.org/docs/)
- [Fluent Bit documentation](https://docs.fluentbit.io/)
