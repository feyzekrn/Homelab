# API Platform

[<- Back to Platform](../README.md)

This directory documents shared API-layer components that are not tied to a single service.

For now this mainly covers GraphQL gateway patterns.

An API platform is the boundary between clients and backend systems. A client can be a web dashboard, mobile app, CLI tool or external integration. Without an API layer, every client would need to know where every internal service lives, which database contains which data and how each internal authentication method works.

A shared API layer hides that internal complexity. It can combine data from multiple services, enforce authentication, translate internal data models into stable client-facing contracts and provide one place for rate limiting, validation and versioning.

This does not mean every homelab needs a large API gateway. Small systems can start with one backend service and normal REST endpoints. The API platform category exists so that the project has a documented place for API aggregation patterns once dashboards and automation services become real.

---

## Why This Matters

The API layer is how clients interact with backend systems. A dashboard, mobile app or external integration usually should not talk directly to every internal service. A shared API layer can aggregate data, enforce authentication and hide internal service topology.

In a homelab, this becomes useful when the admin dashboard needs data from Kubernetes, hardware automation, metrics and user settings. In companies, API layers are used to provide stable contracts, security boundaries and client-specific data access.

---

## What You Can Do With It

- aggregate data for dashboards
- expose a stable API to web and mobile clients
- hide internal service layout
- enforce authentication and authorization
- experiment with GraphQL, REST and gRPC boundaries
- generate typed clients for frontend applications

---

## Common API Patterns

| Pattern | Best fit | Notes |
|---|---|---|
| REST API | Simple services, broad compatibility | Best default for many backend services |
| GraphQL API | Client-driven data shapes, aggregation | Useful for dashboards that combine many sources |
| gRPC | Internal service-to-service contracts | Strong typing and performance, less browser-native |
| API Gateway | Routing, auth, rate limits, edge policies | Can become too heavy if added too early |
| Backend-for-Frontend | One API tailored to one frontend | Useful when web and mobile clients need different shapes |

---

## When This Project Needs It

The project needs a shared API layer when the dashboard starts combining data from multiple places: Kubernetes, hardware control services, metrics summaries, user settings, secret workflows and application state. Until then, each service can expose a small direct API.

The API layer should not become a dumping ground for all business logic. It should aggregate, authorize and shape data for clients while keeping domain logic in the services that own the data.

---

## Components

| Name | Path | Idle RAM | Role |
|---|---|---|---|
| GraphQL | [docs](./graphql) · [chart](../../../helm-charts/infrastructure/platform/api/graphql) · [config](./graphql/terraform) | ~0.1–0.3 GB | GraphQL gateway and schema design experiments |

---

## Learning Links

- [Wikipedia: Application programming interface](https://en.wikipedia.org/wiki/API)
- [Wikipedia: Web API](https://en.wikipedia.org/wiki/Web_API)
- [Wikipedia: Representational state transfer](https://en.wikipedia.org/wiki/REST)
- [Wikipedia: GraphQL](https://en.wikipedia.org/wiki/GraphQL)
- [GraphQL documentation](https://graphql.org/learn/)
