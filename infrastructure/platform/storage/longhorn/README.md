# Longhorn

[<- Back to Storage](../README.md)

Longhorn is the **chosen distributed block storage** for the Kubernetes cluster (`k8s`).

It provides replicated persistent volumes across nodes and gives a clear UI for learning how Kubernetes storage behaves during failures.

**Longhorn is purely a cluster concern.** It has nothing to do with the Proxmox host: it does not manage `pve0`'s disks, it is not the NAS, and the family apps never touch it. Bulk storage lives on the [ZFS pool](../zfs-nas) and reaches its consumers by bind-mount. Longhorn's job is narrower and different — giving cluster pods a volume that survives a node dying.

Longhorn gives Kubernetes workloads persistent block volumes. A pod asks for storage through a PersistentVolumeClaim, and Longhorn can create a volume that is replicated across nodes. If a pod restarts or moves, the volume can be reattached so the workload keeps its data.

For a beginner, Longhorn is useful because it makes Kubernetes storage visible. The UI shows volumes, replicas, health, snapshots, backups and attachment state. That helps explain why storage is more than "mount a folder into a container."

---

## Why It Fits

Longhorn is easier to understand than many production storage systems, but still realistic enough to teach important concepts: replicas, volume health, snapshots, backups, disk scheduling and recovery.

It is a strong homelab choice because it runs inside Kubernetes and works well for learning stateful workloads without immediately operating a full Ceph cluster.

---

## Prerequisites

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../kubernetes/cilium) | Longhorn replicates over the pod network; without a working CNI nothing attaches |
| `open-iscsi` on every node | Longhorn attaches volumes over iSCSI — installed by [Ansible](../../../provisioning/ansible) during provisioning |
| At least **3 nodes** | The default replica count is 3; fewer nodes means degraded volumes by design |
| Free disk space on each node | Replicas consume real capacity — see the sizing reality below |
| [MinIO (backup)](../minio) | Only for Longhorn's own backup target. Not needed to run, needed before data matters |

---

## The Anchor Node Is Excluded — On Purpose

The cluster has one node that is a VM on `pve0` — the [anchor](../../../../setup/compute/README.md#the-bridge-one-node-with-a-foot-in-both-worlds) that keeps critical workloads alive through a cluster rebuild. **Longhorn is deliberately switched off on that node** (`node.longhorn.io/create-default-disk=false`).

Two reasons:

1. **It would be replication on top of replication.** That VM's disk lives on `pve0`, which is itself a ZFS mirror. A Longhorn replica there means three cluster-side copies of data that then get mirrored again — capacity spent twice for no additional safety.
2. **Anchored workloads have no PVCs, by design.** [Keycloak](../../security/rights-management/keycloak) is the reason the anchor exists, and its state lives in a PostgreSQL container on `pve0`, not in a cluster volume. That is the rule rather than a coincidence: **pods on the anchor are stateless, and their state lives in the stable world.** The moment an anchored pod needed a Longhorn volume, it would depend on the cluster again and the anchor would be pointless.

The node still schedules pods normally. It simply does not donate storage.

---

## Sizing Reality

Worth being blunt about, because it constrains what the cluster can hold:

- 3 nodes × 256 GB SATA SSD = **768 GB raw**
- Default 3-way replication → roughly **250 GB usable**, shared by *every* cluster volume

That is enough for databases, application state, [MinIO's app bucket](../minio) and test workloads. It is nowhere near enough for a photo or media library — which is precisely the gap the [ZFS pool](../zfs-nas) fills, and the reason the family apps live beside the cluster instead of on it.

Replica count can be lowered to 2 for volumes that are backed up anyway, trading resilience for capacity. Do that consciously, per StorageClass, not globally.

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

Longhorn is currently `⚫ Inactive`. It runs permanently once the cluster exists, and it is an early component — almost everything stateful on the cluster waits for it. In the build order it comes after [Cilium](../../../kubernetes/cilium) and [MetalLB](../../../kubernetes/metallb), and before [PostgreSQL](../../databases/postgresql), [MinIO](../minio) or any application.

One rule from the Weaknesses above deserves repeating as an operational statement: **replication is not backup.** Three replicas of a dropped table are three copies of a dropped table. [Velero](../../backup/velero) exists for the other half of the problem.

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
