# Messaging

[<- Back to Kubernetes](../README.md)

Messaging systems decouple services. Instead of one service calling another directly for every action, services can publish events or tasks and let other consumers react.

This directory documents NATS, RabbitMQ and Kafka because they teach different messaging models.

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

## Messaging Catalog

| Path | Status | Best fit |
|---|---|---|
| [`./nats`](./nats) | ⚫ Inactive | Lightweight eventing, internal service communication, JetStream |
| [`./rabbitmq`](./rabbitmq) | ⚫ Inactive | Queues, routing patterns, job processing, AMQP ecosystem |
| [`./kafka`](./kafka) | ⚫ Inactive | Durable event logs, replayable streams, stream processing |

---

## Recommendation

Start with NATS for lightweight internal eventing. Add RabbitMQ when the project needs durable job queues, routing exchanges or AMQP compatibility. Add Kafka only when replayable streams, event history or stream processing are the actual learning target.

Do not run all messaging systems permanently unless real workloads need them. They overlap enough that running all of them without a use case mostly creates operational noise.
