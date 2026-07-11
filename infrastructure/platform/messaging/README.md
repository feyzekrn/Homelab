# Messaging

[<- Back to Platform](../README.md)

Messaging systems decouple services. Instead of one service calling another directly for every action, services can publish events or tasks and let other consumers react.

This directory documents NATS, RabbitMQ and Kafka because they teach different messaging models.

Messaging is a way for software systems to communicate without every component calling every other component directly at the same time. One service can publish a message, event or task. Another service can consume it immediately, later, or as part of a worker group.

This matters because direct HTTP calls create tight timing dependencies. If service A calls service B and service B is slow or offline, service A may fail too. With messaging, service A can often record that work needs to happen and continue, while a worker or subscriber handles the work independently.

Different messaging tools solve different problems. A queue distributes jobs to workers. A pub/sub system broadcasts events to subscribers. A stream keeps an ordered history so consumers can replay events. Choosing the wrong model is a common architecture mistake, so this directory documents the tradeoffs explicitly.

---

## Why This Matters

Direct HTTP calls are simple, but they tightly couple services. Messaging gives services another way to communicate: publish an event, enqueue a task or write to a stream. That makes systems more resilient when one part is slow, temporarily offline or needs to process work asynchronously.

In a homelab, messaging is useful once custom services appear. Hardware events, dashboard updates, background jobs and automation triggers are better examples than artificial demo queues.

In companies, messaging is often part of the core architecture. It supports event-driven systems, worker fleets, retries, audit trails, integrations and data pipelines. The important lesson is choosing the right model: NATS for lightweight events, RabbitMQ for queues and Kafka for replayable streams.

---

## What You Can Do With It

- publish hardware and cluster events
- run background workers
- decouple APIs from slow tasks
- retry failed jobs
- build event-driven services
- replay historical events with Kafka
- compare queue-based and stream-based architectures

---

## Main Messaging Models

| Model | Meaning | Good fit |
|---|---|---|
| Queue | A message is processed by one worker from a group | Background jobs, retries, task processing |
| Publish/subscribe | A message is broadcast to interested subscribers | Lightweight events and notifications |
| Stream/event log | Events are stored in ordered logs and can be replayed | Event sourcing, audit trails, analytics pipelines |
| Request/reply | A service sends a request message and waits for a response | Internal service communication without HTTP |

---

## When You Need Messaging

Use messaging when work should happen asynchronously, when multiple consumers need to react to the same event, when failures should be retried, or when an event history has value. Avoid messaging when a simple function call or REST endpoint is clearer. Messaging adds moving parts: broker operations, message schemas, retries, dead letters, ordering, idempotency and monitoring.

For this homelab, good real use cases include hardware power events, dashboard live updates, background media processing, notification retries and event-driven automation.

---

## Messaging Catalog

| Name | Path | Status | Idle RAM | Best fit |
|---|---|---|---|---|
| NATS | [docs](./nats) · [chart](../../../helm-charts/infrastructure/platform/messaging/nats) · [config](./nats/terraform) | ⚫ Inactive | ~20–50 MB | Lightweight eventing, internal service communication, JetStream |
| RabbitMQ | [docs](./rabbitmq) · [chart](../../../helm-charts/infrastructure/platform/messaging/rabbitmq) · [config](./rabbitmq/terraform) | ⚫ Inactive | ~0.15–0.3 GB | Queues, routing patterns, job processing, AMQP ecosystem |
| Kafka | [docs](./kafka) · [chart](../../../helm-charts/infrastructure/platform/messaging/kafka) · [config](./kafka/terraform) | ⚫ Inactive | ~1–2 GB+ | Durable event logs, replayable streams, stream processing |

---

## Recommendation

Start with NATS for lightweight internal eventing. Add RabbitMQ when the project needs durable job queues, routing exchanges or AMQP compatibility. Add Kafka only when replayable streams, event history or stream processing are the actual learning target.

Do not run all messaging systems permanently unless real workloads need them. They overlap enough that running all of them without a use case mostly creates operational noise.

---

## Learning Links

- [Wikipedia: Message queue](https://en.wikipedia.org/wiki/Message_queue)
- [Wikipedia: Publish-subscribe pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)
- [Wikipedia: Event-driven architecture](https://en.wikipedia.org/wiki/Event-driven_architecture)
- [Wikipedia: Apache Kafka](https://en.wikipedia.org/wiki/Apache_Kafka)
- [Wikipedia: RabbitMQ](https://en.wikipedia.org/wiki/RabbitMQ)
