# Redis

[<- Back to Databases](../README.md)

Redis is an in-memory data store commonly used for caching, session storage, rate limiting, lightweight queues and pub/sub. It is the **chosen cache** for this homelab (`k8s`).

It is not a replacement for PostgreSQL, MySQL or MongoDB. In most systems, Redis sits next to a primary database and improves speed or coordination for specific access patterns.

Like [PostgreSQL](../postgresql), it appears in both worlds: a cluster instance for cluster workloads, and a Redis inside each family app's container on `pve0` — [Nextcloud](../../../../applications/nextcloud) uses it for file locking, [Immich](../../../../applications/immich) for its job queue. Same reasoning: each app stays one self-contained backup with no shared dependency.

---

## Prerequisites

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../kubernetes/cilium) | For the cluster instance |
| An application that actually needs it | Redis deployed "in advance" is RAM spent on nothing |
| [Longhorn](../../storage/longhorn) | **Only if** persistence is enabled — see below |
| [Vault](../../security/secret-store) | For the auth password, if exposed beyond one namespace |

**Decide first what is safe to lose.** Redis can run purely in memory (fast, everything gone on restart) or with persistence to disk. For a cache, losing the contents is fine and a volume is wasted overhead. For a job queue — Immich's case — losing the contents means losing queued work. The same software, two entirely different deployment shapes, and the choice belongs to the workload rather than to a default.

Redis stores data primarily in memory, which makes it very fast. Applications use it for data that must be accessed quickly or shared briefly between services: cache entries, login sessions, counters, locks, rate limits and small queues.

Because Redis is often used for short-lived or derived data, it should not be treated like the primary source of truth for important relational state. A common pattern is: PostgreSQL stores durable user data, while Redis stores cached query results or active session data.

Redis supports useful data structures such as strings, hashes, lists, sets, sorted sets and streams. This makes it more than a simple key-value cache, but the project should still be clear about what data is safe to lose and what must be backed up.

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

## Strengths

- Very fast in-memory access.
- Useful built-in data structures.
- Common integration in web frameworks and job libraries.
- Good for sessions, caches and counters.
- Can support lightweight queue and stream patterns.

---

## Weaknesses

- Not the right default for durable relational data.
- Cache invalidation can become a real design problem.
- Persistence and clustering choices need to match the data criticality.
- Distributed locks are easy to misuse without timeouts and ownership rules.
- Message broker features are simpler than RabbitMQ or Kafka.

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

Redis is currently `⚫ Inactive`. It is deployed **on demand, never in advance** — the first real consumers are the family apps on `pve0` (inside their own containers), and the cluster instance follows when a custom service needs caching or sessions.

---

## Operator Note

Evaluate the Redis Operator or Bitnami Redis chart before deciding on a long-term deployment pattern. For learning, start simple before adding clustering.

See also: [`operators`](../../../kubernetes/operators)

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/databases/redis/
```

---

## Learning Links

- [Redis documentation](https://redis.io/docs/latest/)
- [Wikipedia: Redis](https://en.wikipedia.org/wiki/Redis)
- [Wikipedia: Cache](https://en.wikipedia.org/wiki/Cache_(computing))
- [Wikipedia: Key-value database](https://en.wikipedia.org/wiki/Key%E2%80%93value_database)
