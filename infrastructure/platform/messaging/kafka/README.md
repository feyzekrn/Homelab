# Kafka

[<- Back to Messaging](../README.md)

Kafka is a distributed event streaming platform. It stores events in ordered logs called topics, lets consumers read those events at their own pace and supports replaying historical events.

Kafka is not just a queue. It is better understood as an event log that multiple consumers can independently process.

Kafka stores messages as an ordered history. Producers write events to topics. Topics are split into partitions. Consumers read from those partitions and remember their position through offsets.

This is different from a classic queue. In many queue systems, once a worker successfully processes a message, that message is gone from the queue. In Kafka, events are retained for a configured time or size, so another consumer can read the same events later. That makes Kafka useful for audit trails, analytics pipelines, event-driven systems and rebuilding derived views.

For a beginner, the core idea is this: Kafka is valuable when the history of events matters, not only the immediate delivery of work.

---

## Why It Is Documented

Kafka is one of the most important systems in modern backend and data platforms. It is worth documenting even if it should not be the first broker running in this homelab.

For this project, Kafka becomes interesting when the goal is to learn event-driven architecture, stream processing, consumer groups, schema evolution and replayable domain events.

---

## Used For

- durable event streams
- replayable domain events
- event-driven microservice experiments
- stream processing with tools such as Kafka Streams or Flink
- CDC-style data movement from databases
- learning partitions, offsets and consumer groups

---

## Strengths

- Strong model for durable, replayable event logs.
- Multiple consumer groups can independently process the same event history.
- Large ecosystem for stream processing, connectors and data pipelines.
- Good fit for high-throughput event ingestion.
- Supports architectures where derived state can be rebuilt from events.

---

## Weaknesses

- Operationally heavier than NATS or RabbitMQ.
- Concepts such as partitions, offsets, consumer groups and retention need careful learning.
- Not ideal as a simple background job queue.
- Schema design and compatibility become important quickly.
- Small homelab clusters can spend more effort operating Kafka than using it.

---

## Application Examples

- A service writes `hardware.power.changed` events and multiple consumers process them independently.
- A metrics pipeline publishes raw sensor readings before aggregating them elsewhere.
- A dashboard service replays recent cluster events to rebuild a read model.
- A database change-data-capture pipeline sends table changes to downstream consumers.
- A long-running analytics consumer reads events without blocking operational services.

---

## Alternatives

| Alternative | Notes |
|---|---|
| NATS JetStream | Much lighter and easier for small event-driven systems |
| RabbitMQ | Better for work queues, retries and task routing |
| Redpanda | Kafka-compatible with simpler operations for smaller clusters |
| Redis Streams | Useful for smaller stream workloads when Redis is already present |

---

## Comparison Notes

Kafka is the right tool when event history matters. Consumers track offsets and can replay past events. RabbitMQ is more focused on delivering work to consumers. NATS is usually easier for lightweight pub/sub. Redis Streams can cover smaller stream use cases, but Kafka has the strongest ecosystem for event streaming.

---

## Runtime Status

Kafka is currently `⚫ Inactive`. Do not run it by default. Add it when stream processing or event replay is a concrete learning goal.

---

## Operator Note

Evaluate Strimzi before deploying Kafka manually. Kafka has enough moving parts that an operator is usually the better learning path.

See also: [`../../operators`](../../../kubernetes/operators)

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/messaging/kafka/
```

---

## Learning Links

- [Apache Kafka documentation](https://kafka.apache.org/documentation/)
- [Wikipedia: Apache Kafka](https://en.wikipedia.org/wiki/Apache_Kafka)
- [Wikipedia: Event-driven architecture](https://en.wikipedia.org/wiki/Event-driven_architecture)
- [Wikipedia: Change data capture](https://en.wikipedia.org/wiki/Change_data_capture)
