# Longhorn

[<- Back to Kubernetes Storage](../README.md)

Longhorn is the recommended distributed block storage system for the first Kubernetes phase.

It provides replicated persistent volumes across nodes and gives a clear UI for learning how Kubernetes storage behaves during failures.

Longhorn gives Kubernetes workloads persistent block volumes. A pod asks for storage through a PersistentVolumeClaim, and Longhorn can create a volume that is replicated across nodes. If a pod restarts or moves, the volume can be reattached so the workload keeps its data.

For a beginner, Longhorn is useful because it makes Kubernetes storage visible. The UI shows volumes, replicas, health, snapshots, backups and attachment state. That helps explain why storage is more than "mount a folder into a container."

---

## Why It Fits

Longhorn is easier to understand than many production storage systems, but still realistic enough to teach important concepts: replicas, volume health, snapshots, backups, disk scheduling and recovery.

It is a strong homelab choice because it runs inside Kubernetes and works well for learning stateful workloads without immediately operating a full Ceph cluster.

---

## Used For

- persistent volumes for PostgreSQL
- persistent volumes for MySQL
- persistent volumes for MongoDB
- test workloads that need durable storage
- backup and restore practice
- learning volume replicas and failure recovery

---

## Strengths

- Approachable UI for understanding storage health.
- Kubernetes-native volume provisioning.
- Replication across nodes for better resilience than single-node local paths.
- Snapshot and backup concepts are visible.
- Good first storage platform for a bare-metal homelab.

---

## Weaknesses

- Still requires healthy disks, reliable networking and careful resource planning.
- Replication is not the same as backup; deleted or corrupted data can replicate too.
- Performance depends on hardware, network and replica count.
- It is simpler than Ceph but still operationally important once real data is stored.

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
../../../../helm-charts/infrastructure/platform/storage/longhorn/
```

---

## Learning Links

- [Longhorn documentation](https://longhorn.io/docs/)
- [Kubernetes Persistent Volumes documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Wikipedia: Block-level storage](https://en.wikipedia.org/wiki/Block-level_storage)
- [Wikipedia: Data replication](https://en.wikipedia.org/wiki/Replication_(computing))
