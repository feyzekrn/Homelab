# Runtime Platform

[<- Back to Platform](../README.md)

Runtime platform components sit between applications and Kubernetes. They can provide service invocation, sidecars, traffic policy, mTLS, retries or state abstractions.

These tools are powerful, but they should be added carefully. They can teach useful production patterns, but they also increase cluster complexity.

Dapr lives here under [`dapr`](./dapr) because it is a distributed application runtime. It can use service-mesh-like sidecars, but its main purpose is application building blocks such as pub/sub, state stores and bindings.

Kubernetes runs containers, schedules pods and exposes Services. It does not automatically decide how application code should call other services, publish events, read secrets, store state, retry failed calls or enforce mutual TLS between workloads.

Runtime platform tools add shared behavior around applications. Some tools are application-facing, meaning developers call their APIs. Dapr is in this category. Other tools are network-facing, meaning they transparently manage traffic between services. Service meshes are in this category.

These tools are useful after the basic platform works. Adding them too early can hide the fundamentals and make debugging harder.

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

| Name | Path | Role |
|---|---|---|
| Dapr | [docs](./dapr) · [chart](../../../helm-charts/infrastructure/platform/runtime/dapr) · [config](./dapr/terraform) | Distributed application runtime |
| Service Mesh | [docs](./service-mesh) · [chart](../../../helm-charts/infrastructure/platform/runtime/service-mesh) · [config](./service-mesh/terraform) | Traffic management and service-to-service security |

---

## Dapr vs Service Mesh

| Topic | Dapr | Service mesh |
|---|---|---|
| Main audience | Application developers | Platform/network operators |
| Primary model | App calls Dapr APIs | Proxy manages service traffic |
| Typical features | Pub/sub, state, bindings, secrets, service invocation | mTLS, retries, traffic splitting, policy, observability |
| Code changes | Usually yes | Often minimal |
| Homelab timing | After custom services exist | Later, when traffic policy or mTLS is needed |

---

## Learning Links

- [Dapr documentation](https://docs.dapr.io/)
- [Wikipedia: Service mesh](https://en.wikipedia.org/wiki/Service_mesh)
- [Wikipedia: Sidecar pattern](https://en.wikipedia.org/wiki/Sidecar_pattern)
- [Wikipedia: Mutual authentication](https://en.wikipedia.org/wiki/Mutual_authentication)
