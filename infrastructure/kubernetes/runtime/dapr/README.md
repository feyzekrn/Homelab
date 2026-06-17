# Dapr

[<- Back to Runtime Platform](../README.md)

Dapr is a distributed application runtime. It gives services building blocks such as service invocation, pub/sub, state stores, bindings and secrets through sidecars and APIs.

Dapr is not exactly the same thing as a service mesh. It overlaps with some service-to-service concerns, but it is more focused on application building blocks than transparent network traffic management.

---

## Why It Fits

Dapr is interesting for this homelab because the project will likely include Go services, hardware automation and event-driven workflows. Dapr can make it easier to swap messaging systems, state stores and bindings while keeping application code cleaner.

---

## Used For

- pub/sub abstraction over NATS or RabbitMQ
- service invocation between internal services
- secret access abstraction over the configured Secret Store
- state store experiments
- bindings for external or hardware-triggered events
- learning sidecar-based application runtime patterns

---

## Application Examples

- A Go service publishes hardware events through Dapr pub/sub while the backend can later switch from NATS to RabbitMQ.
- A dashboard API invokes an internal node-control service through Dapr service invocation.
- A service reads credentials from the Secret Store through Dapr without importing the provider SDK directly.
- A hardware automation worker stores short-lived state through a Dapr state component backed by Redis.
- A future mobile app triggers cluster actions without knowing the direct internal service address.
- A service consumes external events through Dapr bindings instead of custom integration code.

---

## Alternatives

| Alternative | Notes |
|---|---|
| Plain Kubernetes services | Simpler and usually enough at the beginning |
| Linkerd | Real service mesh, focused on traffic and mTLS |
| Istio | Powerful service mesh, heavier operational model |
| Direct SDK integrations | Less platform abstraction, more application coupling |

---

## Comparison Notes

Dapr is application-facing. It gives developers APIs for pub/sub, service invocation, state, secrets and bindings. A service mesh is network-facing. It manages traffic, mTLS, retries and observability without requiring the application to call Dapr APIs. Plain Kubernetes services are simpler and should be enough until the project has multiple custom services.

---

## Runtime Status

Dapr is currently `⚫ Inactive`. Keep it as a research topic until there are several custom services that benefit from its building blocks.

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`, but the basic upstream Helm flow is:

```bash
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update
helm install dapr dapr/dapr --namespace dapr-system --create-namespace
```

After installing, test one small service with Dapr service invocation, then add a Secret Store component and read one non-production test secret through the Dapr Secrets API.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/runtime/dapr/
```

---

## Documentation

- [Dapr Kubernetes hosting documentation](https://docs.dapr.io/operations/hosting/kubernetes/)
- [Dapr Secrets API](https://docs.dapr.io/developing-applications/building-blocks/secrets/)
