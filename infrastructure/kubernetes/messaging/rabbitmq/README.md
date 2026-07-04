# RabbitMQ

[<- Back to Messaging](../README.md)

RabbitMQ is a mature message broker built around queues, exchanges and routing patterns.

It is useful when services need reliable task processing, delayed jobs, routing keys or AMQP compatibility.

RabbitMQ is a broker for messages that need to be delivered to consumers. A producer sends a message to an exchange, the exchange routes it to one or more queues, and workers consume messages from those queues.

The queue model is useful when work should be processed by one worker from a group. For example, if 100 image-resize jobs are waiting, ten workers can share the queue and process the jobs in parallel. If a worker fails, RabbitMQ can redeliver unacknowledged messages.

RabbitMQ is also known for routing patterns. Exchanges, routing keys and bindings let a system route messages based on topics or rules. This makes RabbitMQ stronger than a simple queue library when applications need retries, dead-letter queues, delayed processing or AMQP ecosystem support.

---

## Why It Fits

RabbitMQ is common in real full-stack systems. Running it in the homelab is useful for learning worker queues, retry behavior, dead-letter queues and operational visibility.

It is also a good comparison point against NATS and Kafka. NATS teaches lightweight eventing. Kafka teaches replayable event logs. RabbitMQ teaches broker-centered message delivery and job processing.

---

## Used For

- background jobs
- task queues
- retry and dead-letter patterns
- AMQP-based service communication
- comparison against NATS
- worker fleet experiments

---

## Strengths

- Mature queue and broker semantics.
- Strong routing model through exchanges, routing keys and bindings.
- Good support for acknowledgements and redelivery.
- Dead-letter queues make failed-message workflows explicit.
- Many frameworks and languages support AMQP and RabbitMQ integrations.

---

## Weaknesses

- It is not a replayable event log in the same way Kafka is.
- Complex routing can become hard to reason about if naming is undisciplined.
- High-throughput stream analytics are usually a better fit for Kafka or similar systems.
- Clustering and persistent queues require operational care.

---

## Application Examples

- A media-processing worker consumes image resize jobs from a queue.
- A notification service retries failed email or webhook delivery.
- A billing-style workflow uses dead-letter queues for messages that cannot be processed.
- A backend separates slow tasks from the request path by publishing jobs after an API call.
- Multiple workers scale horizontally by consuming from the same queue.

---

## Alternatives

| Alternative | Notes |
|---|---|
| NATS JetStream | Smaller and simpler for event streams |
| Kafka | Better for high-throughput event logs |
| Redis queues | Simple and common, less feature-rich as a broker |

---

## Comparison Notes

RabbitMQ is a broker for messages that should be delivered to consumers. Kafka is an event log where consumers can replay history. NATS is lighter and often easier for internal eventing. Redis queues are convenient, but RabbitMQ has richer routing, acknowledgements and dead-letter behavior.

---

## Runtime Status

RabbitMQ is currently `⚫ Inactive`. Add it when a workload needs classic broker semantics.

---

## Operator Note

Evaluate RabbitMQ Cluster Kubernetes Operator for production-style deployment.

See also: [`../../operators`](../../operators)

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/messaging/rabbitmq/
```

---

## Learning Links

- [RabbitMQ documentation](https://www.rabbitmq.com/docs)
- [Wikipedia: RabbitMQ](https://en.wikipedia.org/wiki/RabbitMQ)
- [Wikipedia: Advanced Message Queuing Protocol](https://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol)
- [Wikipedia: Message queue](https://en.wikipedia.org/wiki/Message_queue)
