# GraphQL

[<- Back to API Platform](../README.md)

GraphQL is an API query language and runtime pattern where clients request exactly the data shape they need.

In this homelab, GraphQL is best treated as an application-facing API layer, not as a replacement for internal service boundaries.

With a traditional REST API, the server usually defines fixed endpoints such as `/users`, `/nodes` or `/services/123/events`. Each endpoint returns the shape the backend developer chose. That is often simple and correct.

GraphQL changes the interaction. The server exposes a typed schema, and the client sends a query describing the fields it wants. A dashboard can ask for a node name, health state, latest events and related service status in one request instead of making several endpoint calls.

This is powerful for frontend-heavy applications, but it also introduces responsibility. The schema becomes a product contract. Authorization must be enforced field by field where needed, expensive queries must be controlled, and backend ownership must stay clear.

---

## Why It Fits

GraphQL can be useful for a dashboard that combines data from several internal services: cluster state, hardware state, metrics summaries and user-facing admin actions.

It is a good fit when the frontend needs flexible data shapes and when the backend can provide a carefully designed schema. It is not automatically better than REST for every service. Many internal services should still use REST or gRPC because they are simpler and easier to debug.

---

## Used For

- admin dashboard API
- aggregating multiple backend services
- strongly typed frontend data access
- experimenting with schema design

---

## Strengths

- Clients can request exactly the fields they need.
- A typed schema gives frontend and backend developers a shared contract.
- Good for dashboards that combine data from many internal systems.
- Reduces over-fetching and under-fetching when REST endpoints do not match UI needs.
- Tooling can generate typed clients and schema documentation.

---

## Weaknesses

- Authorization can be more subtle than endpoint-based REST.
- Query complexity needs limits so one request cannot overload many backends.
- Caching is less straightforward than simple REST endpoints.
- It can hide service boundaries if everything is forced through one graph too early.
- It is unnecessary for small services with simple CRUD endpoints.

---

## Application Examples

- The dashboard asks for cluster nodes, active alerts and recent hardware events in one request.
- A frontend receives strongly typed data from generated GraphQL types.
- A GraphQL resolver calls a Kubernetes inventory service and a metrics summary service.
- Admin-only mutations are protected through Keycloak roles.
- A query depth limit prevents expensive nested queries from overwhelming backend services.

---

## Alternatives

| Alternative | Notes |
|---|---|
| REST | Simpler default for many services |
| gRPC | Strong internal service-to-service option |
| tRPC | Excellent TypeScript full-stack option, less language-neutral |

---

## Runtime Status

GraphQL is currently `⚫ Inactive`. Add it when the dashboard or API layer needs aggregation.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/api/graphql/
```

---

## Learning Links

- [Wikipedia: GraphQL](https://en.wikipedia.org/wiki/GraphQL)
- [GraphQL documentation](https://graphql.org/learn/)
- [Wikipedia: API](https://en.wikipedia.org/wiki/API)
- [Wikipedia: Backend for frontend](https://en.wikipedia.org/wiki/Backend_for_frontend_pattern)
