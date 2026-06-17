# Runtime Platform

[<- Back to Kubernetes](../README.md)

Runtime platform components sit between applications and Kubernetes. They can provide service invocation, sidecars, traffic policy, mTLS, retries or state abstractions.

These tools are powerful, but they should be added carefully. They can teach useful production patterns, but they also increase cluster complexity.

Dapr lives here under [`dapr`](./dapr) because it is a distributed application runtime. It can use service-mesh-like sidecars, but its main purpose is application building blocks such as pub/sub, state stores and bindings.

---

## Why This Matters

Kubernetes runs containers, but it does not automatically solve every application concern. Applications still need service calls, retries, pub/sub, state access, secrets, bindings and traffic policy. Runtime tools provide reusable patterns for those concerns.

In a homelab, runtime tools should come after plain Kubernetes services are understood. In companies, runtimes and meshes can standardize cross-cutting concerns across many teams, but they also add operational complexity.

---

## What You Can Do With It

- abstract pub/sub behind Dapr
- read secrets through a runtime API
- experiment with service invocation
- add mTLS and traffic policy through a mesh
- compare app-facing and network-facing abstractions
- avoid baking every integration directly into application code

---

## Components

| Path | Role |
|---|---|
| [`./dapr`](./dapr) | Distributed application runtime |
| [`./service-mesh`](./service-mesh) | Traffic management and service-to-service security |
