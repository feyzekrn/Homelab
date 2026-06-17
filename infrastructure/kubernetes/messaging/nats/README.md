# NATS

[<- Back to Messaging](../README.md)

NATS is a lightweight messaging system for service-to-service communication.

It supports simple pub/sub and, with JetStream, persistent streams and durable consumers.

---

## Why It Fits

NATS fits this homelab because it is small, fast and easy to reason about. It is a good match for internal events such as hardware state changes, cluster automation triggers and real-time dashboard updates.

---

## Used For

- internal event distribution
- hardware automation events
- async communication between Go services
- dashboard live updates
- JetStream experiments

---

## Application Examples

- A hardware monitor publishes `node.temperature.changed` events.
- A power controller subscribes to `node.power.requested` commands.
- The dashboard receives live cluster events without polling REST endpoints.
- A Go service publishes domain events after writing state to PostgreSQL.
- JetStream stores recent automation events so consumers can recover after restarts.

---

## Alternatives

| Alternative | Notes |
|---|---|
| RabbitMQ | Better for classic queue and routing patterns |
| Kafka | Powerful, but too heavy for the initial homelab scope |
| Redis Streams | Useful if Redis is already part of the stack |

---

## Comparison Notes

NATS is best when the system needs simple, fast communication with low operational overhead. RabbitMQ is usually better for task queues with routing and retries. Kafka is better when event history, replay and stream processing are central requirements.

---

## Runtime Status

NATS is currently `⚫ Inactive`. Keep it documented and ready, but run it when a service actually needs eventing.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/messaging/nats/
```
