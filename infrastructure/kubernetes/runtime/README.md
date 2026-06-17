# Runtime Platform

[<- Back to Kubernetes](../README.md)

Runtime platform components sit between applications and Kubernetes. They can provide service invocation, sidecars, traffic policy, mTLS, retries or state abstractions.

These tools are powerful, but they should be added carefully. They can teach useful production patterns, but they also increase cluster complexity.

Dapr lives here under [`dapr`](./dapr) because it is a distributed application runtime. It can use service-mesh-like sidecars, but its main purpose is application building blocks such as pub/sub, state stores and bindings.

---

## Components

| Component | Role | Documentation |
|---|---|---|
| Dapr | Distributed application runtime | [dapr](./dapr) |
| Service mesh | Traffic management and service-to-service security | [service-mesh](./service-mesh) |
