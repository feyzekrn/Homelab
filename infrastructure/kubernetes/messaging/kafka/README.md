# Kafka

[<- Back to Messaging](../README.md)

Kafka is a distributed event streaming platform. It stores events in ordered logs called topics, lets consumers read those events at their own pace and supports replaying historical events.

Kafka is not just a queue. It is better understood as an event log that multiple consumers can independently process.

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

See also: [`../../operators`](../../operators)

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/messaging/kafka/
```
