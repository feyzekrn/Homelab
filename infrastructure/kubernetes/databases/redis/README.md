# Redis

[<- Back to Databases](../README.md)

Redis is an in-memory data store commonly used for caching, session storage, rate limiting, lightweight queues and pub/sub.

It is not a replacement for PostgreSQL, MySQL or MongoDB. In most systems, Redis sits next to a primary database and improves speed or coordination for specific access patterns.

---

## Why It Fits

Redis is part of many real full-stack systems. It is useful for learning how applications handle fast ephemeral data, cache invalidation, background job coordination and distributed rate limits.

In this homelab, Redis is especially useful once dashboards, APIs or automation services need low-latency shared state.

---

## Used For

- API response caching
- user session storage
- rate limiting counters
- distributed locks with careful timeouts
- lightweight queues
- pub/sub for simple events
- temporary state for dashboards and background workers

---

## Application Examples

- A Next.js dashboard caches expensive cluster summary queries for a few seconds.
- An API stores login sessions or refresh-token metadata in Redis.
- A rate limiter counts requests per user or IP address.
- A background worker consumes small jobs from a Redis-backed queue.
- A hardware automation service stores short-lived node health state.

---

## Alternatives

| Alternative | Notes |
|---|---|
| PostgreSQL | Better for durable relational data |
| MongoDB | Better for persistent document data |
| RabbitMQ | Better for robust queue semantics and retries |
| NATS | Better for lightweight service events |
| Memcached | Simpler cache-only option |

---

## Comparison Notes

Redis is best for fast, short-lived or cache-like data. PostgreSQL and MySQL should hold important durable relational state. MongoDB should hold durable document data. RabbitMQ and NATS are usually better choices when messaging semantics matter more than key-value access.

---

## Runtime Status

Redis is currently `⚫ Inactive`. Add it when a real application needs caching, sessions, rate limiting or lightweight queue patterns.

---

## Operator Note

Evaluate the Redis Operator or Bitnami Redis chart before deciding on a long-term deployment pattern. For learning, start simple before adding clustering.

See also: [`../../operators`](../../operators)

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/databases/redis/
```
