# GraphQL

[<- Back to API Platform](../README.md)

GraphQL is an API query language and runtime pattern where clients request exactly the data shape they need.

In this homelab, GraphQL is best treated as an application-facing API layer, not as a replacement for internal service boundaries.

---

## Why It Fits

GraphQL can be useful for a dashboard that combines data from several internal services: cluster state, hardware state, metrics summaries and user-facing admin actions.

---

## Used For

- admin dashboard API
- aggregating multiple backend services
- strongly typed frontend data access
- experimenting with schema design

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
