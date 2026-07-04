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

| Path | Role |
|---|---|
| [`./fluent-bit`](./fluent-bit) | Lightweight log collector on nodes |
| [`./opensearch`](./opensearch) | Search and analytics backend similar to Elasticsearch |

---

## Recommended Direction

Use Fluent Bit for collection and OpenSearch for storage and search.

This is similar to an ELK-style setup, but avoids tying the project too early to a heavier Elasticsearch and Logstash deployment. Loki should also remain a serious alternative if the goal is a lighter Kubernetes-native log backend.

---

## Learning Links

- [Wikipedia: Logging](https://en.wikipedia.org/wiki/Logging_(computing))
- [Wikipedia: Elasticsearch](https://en.wikipedia.org/wiki/Elasticsearch)
- [OpenSearch documentation](https://opensearch.org/docs/)
- [Fluent Bit documentation](https://docs.fluentbit.io/)
