# RabbitMQ

[<- Back to Messaging](../README.md)

RabbitMQ is a mature message broker built around queues, exchanges and routing patterns.

It is useful when services need reliable task processing, delayed jobs, routing keys or AMQP compatibility.

---

## Why It Fits

RabbitMQ is common in real full-stack systems. Running it in the homelab is useful for learning worker queues, retry behavior, dead-letter queues and operational visibility.

---

## Used For

- background jobs
- task queues
- retry and dead-letter patterns
- AMQP-based service communication
- comparison against NATS

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
