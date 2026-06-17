# Logging

[<- Back to Observability](../README.md)

Logs are event records emitted by applications and infrastructure components.

The goal is not just to store logs, but to make failures searchable and understandable.

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

This is similar to an ELK-style setup, but avoids tying the project too early to a heavier Elasticsearch and Logstash deployment.
