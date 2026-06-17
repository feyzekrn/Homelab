# Longhorn

[<- Back to Kubernetes Storage](../README.md)

Longhorn is the recommended distributed block storage system for the first Kubernetes phase.

It provides replicated persistent volumes across nodes and gives a clear UI for learning how Kubernetes storage behaves during failures.

---

## Why It Fits

Longhorn is easier to understand than many production storage systems, but still realistic enough to teach important concepts: replicas, volume health, snapshots, backups, disk scheduling and recovery.

---

## Used For

- persistent volumes for PostgreSQL
- persistent volumes for MySQL
- persistent volumes for MongoDB
- test workloads that need durable storage
- backup and restore practice

---

## Alternatives

| Alternative | Notes |
|---|---|
| OpenEBS | Good Kubernetes-native storage option |
| Rook/Ceph | Powerful, but operationally heavier |
| local-path-provisioner | Simple, but does not solve node failure |
| NFS | Easy to start, but hides many Kubernetes storage lessons |

---

## Runtime Status

Longhorn is currently `⚫ Inactive`. It should run permanently once stateful workloads are deployed.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/platform/longhorn/
```
