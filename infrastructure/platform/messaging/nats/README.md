# NATS

[<- Back to Messaging](../README.md)

NATS is a lightweight messaging system for service-to-service communication.

It supports simple publish/subscribe messaging and, with JetStream, persistent streams and durable consumers.

NATS is a small, fast message broker. A service can publish a message on a subject such as `node.temperature.changed`, and other services can subscribe to that subject. The publisher does not need to know who is listening.

Without JetStream, NATS is mainly about live communication: messages move quickly through the system, but the broker is not primarily acting as a long-term database. With JetStream, NATS can persist streams, allow consumers to replay messages and support more durable workflows.

For beginners, NATS is a good first messaging system because the basic model is easy to understand: subjects, publishers, subscribers and optional persistence.

---

## Why It Fits

NATS fits this homelab because it is small, fast and easy to reason about. It is a good match for internal events such as hardware state changes, cluster automation triggers and real-time dashboard updates.

It is also useful for Go services and automation code because clients are simple and the operational footprint is smaller than Kafka or a large AMQP broker. That makes it a better first eventing system for a homelab where the goal is to learn without adding too much permanent maintenance.

---

## Used For

- internal event distribution
- hardware automation events
- async communication between Go services
- dashboard live updates
- JetStream experiments
- lightweight request/reply communication

---

## Strengths

- Very lightweight compared with Kafka and many enterprise brokers.
- Simple subject-based publish/subscribe model.
- Good latency characteristics for internal service communication.
- JetStream adds persistence when durable consumers are needed.
- Works well for event-driven automation and live dashboard updates.

---

## Weaknesses

- It is not the best choice for complex AMQP routing patterns.
- Kafka has a larger ecosystem for stream processing and event-log analytics.
- Durable JetStream design still requires understanding retention, acknowledgements and consumer state.
- It can be too minimal if the workload really needs rich queue semantics, exchanges or mature dead-letter workflows.

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
../../../../helm-charts/infrastructure/platform/messaging/nats/
```

---

## Learning Links

- [NATS documentation](https://docs.nats.io/)
- [NATS JetStream documentation](https://docs.nats.io/nats-concepts/jetstream)
- [Wikipedia: Publish-subscribe pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)
- [Wikipedia: Message queue](https://en.wikipedia.org/wiki/Message_queue)
