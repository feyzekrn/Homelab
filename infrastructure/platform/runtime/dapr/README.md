# Dapr

[<- Back to Runtime Platform](../README.md)

Dapr is a distributed application runtime. It gives services building blocks such as service invocation, pub/sub, state stores, bindings and secrets through sidecars and APIs.

Dapr is not exactly the same thing as a service mesh. It overlaps with some service-to-service concerns, but it is more focused on application building blocks than transparent network traffic management.

Dapr gives applications a set of common APIs for distributed-system tasks. Instead of every service directly importing a NATS client, Redis client, secret-store SDK and custom retry logic, the service can call Dapr APIs. Dapr then talks to the configured backend components.

For example, an application can publish an event through Dapr pub/sub. Today the backend might be NATS. Later it might be RabbitMQ. The application code can stay closer to the Dapr API instead of being tightly coupled to one broker.

Dapr usually runs as a sidecar next to the application. The app talks to the sidecar, and the sidecar talks to the configured infrastructure.

---

## Why It Fits

Dapr is interesting for this homelab because the project will likely include Go services, hardware automation and event-driven workflows. Dapr can make it easier to swap messaging systems, state stores and bindings while keeping application code cleaner.

It also gives a practical way to learn distributed application patterns without immediately writing custom integration code for every backend.

---

## Used For

- pub/sub abstraction over NATS or RabbitMQ
- service invocation between internal services
- secret access abstraction over the configured Secret Store
- state store experiments
- bindings for external or hardware-triggered events
- learning sidecar-based application runtime patterns

---

## Strengths

- Provides common APIs for recurring distributed application concerns.
- Decouples application code from some backend-specific SDKs.
- Supports many components for pub/sub, state and secrets.
- Useful for event-driven and automation-heavy services.
- Can improve consistency across services written in different languages.

---

## Weaknesses

- Adds sidecars and platform components that must be operated.
- Application code still needs to understand Dapr's programming model.
- It can be unnecessary for a small number of simple services.
- It does not replace all service-mesh traffic features.
- Debugging includes both app behavior and Dapr component configuration.

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
../../../../helm-charts/infrastructure/platform/runtime/dapr/
```

---

## Documentation

- [Dapr Kubernetes hosting documentation](https://docs.dapr.io/operations/hosting/kubernetes/)
- [Dapr Secrets API](https://docs.dapr.io/developing-applications/building-blocks/secrets/)
- [Wikipedia: Sidecar pattern](https://en.wikipedia.org/wiki/Sidecar_pattern)
- [Wikipedia: Event-driven architecture](https://en.wikipedia.org/wiki/Event-driven_architecture)
