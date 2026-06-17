# Messaging

[<- Back to Kubernetes](../README.md)

Messaging systems decouple services. Instead of one service calling another directly for every action, services can publish events or tasks and let other consumers react.

This directory documents NATS, RabbitMQ and Kafka because they teach different messaging models.

---

## Messaging Catalog

| System | Status | Best fit | Documentation |
|---|---|---|---|
| NATS | ⚫ Inactive | Lightweight eventing, internal service communication, JetStream | [nats](./nats) |
| RabbitMQ | ⚫ Inactive | Queues, routing patterns, job processing, AMQP ecosystem | [rabbitmq](./rabbitmq) |
| Kafka | ⚫ Inactive | Durable event logs, replayable streams, stream processing | [kafka](./kafka) |

---

## Recommendation

Start with NATS for lightweight internal eventing. Add RabbitMQ when the project needs durable job queues, routing exchanges or AMQP compatibility. Add Kafka only when replayable streams, event history or stream processing are the actual learning target.

Do not run all messaging systems permanently unless real workloads need them. They overlap enough that running all of them without a use case mostly creates operational noise.
