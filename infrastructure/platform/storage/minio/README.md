# MinIO

[<- Back to Storage](../README.md)

MinIO provides S3-compatible object storage.

In this homelab, MinIO fills **two roles with opposite requirements** — which is why it is deployed **twice**, once in each world.

| Instance | Runs on | Serves | Requirement that forces the placement |
|---|---|---|---|
| `minio-apps` | `k8s` | Application buckets: uploads, images, exports, S3 development | Must be **next to the applications** — low latency, same failure domain, reachable by cluster Services |
| `minio-backup` | `lxc` on [`pve0`](../../../../setup/compute/proxmox-cluster) | [Velero](../../backup/velero) and Longhorn backup target | Must **outlive the cluster** it protects |

Collapsing these into one instance is the mistake worth naming: a backup stored inside the failure domain it protects is not a backup. Wipe the cluster to rebuild it and the restore path goes with it. But the reverse is equally wrong — routing every application's object storage through a container on the hypervisor adds a network hop and a cross-world dependency to a workload that has no reason to leave the cluster.

Two instances, two buckets, two purposes. This is also normal practice outside homelabs: nobody uses their backup bucket as their application bucket.

Object storage stores data as objects inside buckets. Applications access those objects through an API instead of mounting a disk. This is the model popularized by Amazon S3, and many modern applications know how to talk to S3-compatible storage.

MinIO provides that kind of API in a self-hosted form. A service can upload a file to a bucket, read it later through an object key and manage access through credentials and bucket policies.

Object storage is different from block storage. A database usually wants block storage. Backups, artifacts, exports and file uploads often fit object storage better.

---

## Why It Fits

MinIO is the homelab S3 equivalent. It gives applications an S3-compatible endpoint without requiring AWS, and it is easy to understand compared to larger distributed object-storage platforms.

For this project it serves three jobs, in order of importance:

1. **The backup target.** [Velero](../../backup/velero) speaks S3, and so does Longhorn's backup mechanism. MinIO is what makes `tank/backups` look like a bucket.
2. **Object storage for applications** that prefer S3 over a mounted volume.
3. **A local S3 to develop against**, so custom services can use the same SDK shape they would use in a cloud.

---

## How Each Instance Is Built

### `minio-apps` — on the cluster

| | |
|---|---|
| **Runs on** | `k8s` |
| **Storage** | A single [Longhorn](../longhorn) volume |
| **Replicas** | **One.** Availability comes from Longhorn, not from MinIO |

The instinct is to run MinIO in its distributed mode for high availability. That is the wrong shape here for two reasons: distributed MinIO wants at least four drives for erasure coding, and layering it on Longhorn means **replication on top of replication** — Longhorn already keeps three copies, and MinIO's erasure coding would multiply that again on 256 GB SSDs.

The correct pattern is a single MinIO pod on a Longhorn volume. If the node dies, Longhorn's replica set keeps the volume intact and Kubernetes reschedules the pod elsewhere. That is exactly the availability behaviour wanted, at one third of the storage cost.

**Capacity is the real constraint.** Three 256 GB SATA SSDs leave roughly 250 GB usable after Longhorn replication — for *every* cluster volume, not just this one. `minio-apps` is therefore sized for metadata, thumbnails, exports and uploads measured in gigabytes. Immich's photo originals can never live here; they belong on the ZFS pool by bind-mount.

### `minio-backup` — on the Proxmox host

| | |
|---|---|
| **Runs on** | `lxc` on [`pve0`](../../../../setup/compute/proxmox-cluster) |
| **Storage** | `tank/backups` on the [ZFS pool](../zfs-nas) |
| **Reached by** | Velero and Longhorn from the cluster, over the storage VLAN |

This one exists purely so the restore path survives the thing it restores. It also inherits ZFS snapshots for free, which means an accidental bucket deletion is recoverable — not only a node failure.

The honest limit: `pve0` is still one box in one flat. It protects against cluster mistakes, not against fire or theft. That is what the `zfs send` copy off the machine is for, documented in [zfs-nas](../zfs-nas#operational-notes).

---

## Prerequisites

**`minio-apps`:**

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../kubernetes/cilium) | Pod networking has to work before anything schedules |
| [Longhorn](../longhorn) | Provides the persistent volume and the availability behaviour |
| [Traefik](../../ingress/traefik) + [cert-manager](../../ingress/cert-manager) | Only if the console or S3 endpoint is reachable by hostname |
| [Vault](../../security/secret-store) | Access keys belong in the secret store, not in a values file |

**`minio-backup`:**

| Requirement | Why |
|---|---|
| **Physical disks in `pve0`** | The ZFS pool does not exist yet — this is the hard blocker |
| [`zfs-nas`](../zfs-nas) with the `tank/backups` dataset | The data directory it bind-mounts |
| Network path from the cluster VLAN | Velero pushes backups from inside the cluster |

### The gap worth stating plainly

`pve0` currently holds one NVMe carrying the hypervisor, so `minio-backup` cannot exist yet — and until it does, **the cluster has no proper backup target.** Anything built before the disks arrive is running without a restore path.

That is an acceptable risk only while nothing irreplaceable is stored. It stops being acceptable the moment the first real data lands, which makes disks a prerequisite for the family apps rather than a nice-to-have. Until then, manual exports to an external disk are the honest stopgap — not a substitute.

---

## Used For

- application object storage
- backup targets
- artifact storage
- S3-compatible development and testing
- storing uploads from services
- testing S3 SDK integrations

---

## Strengths

- Strong S3-compatible API for self-hosted environments.
- Useful for Velero-style backup targets and application uploads.
- Easier to reason about than larger object-storage platforms.
- Good local development substitute for cloud S3.
- Integrates with many SDKs and tools that already support S3.

---

## Weaknesses

- It is not a POSIX filesystem replacement.
- Bucket policies and credentials still need security design.
- Distributed production-style MinIO requires careful disk and node planning.
- It should not be treated as the only backup location if it runs in the same failure domain as the cluster.

---

## Application Examples

- A dashboard stores exported reports in a private bucket.
- Velero or another backup tool writes backups to an S3-compatible target.
- A service stores user-uploaded files without putting them into PostgreSQL.
- CI publishes generated artifacts into a bucket.
- Local development uses the same S3 API shape as production-style object storage.

---

## Runtime Status

Both instances are `⚫ Inactive`, and they arrive at different times:

- **`minio-apps`** comes with the cluster, once Longhorn works. It is what unblocks any application expecting an S3 endpoint, so it is early.
- **`minio-backup`** is blocked on hardware — it cannot exist before `pve0` has disks. It must be running **before the first irreplaceable data**, which makes it a gate on deploying the family apps rather than a later cleanup task.

---

## Alternatives

| Alternative | Location | Homelab fit | Business fit | Notes |
|---|---|---|---|---|
| MinIO | Self-hosted | Recommended | Good for many private platforms | Strong S3 compatibility and simple operational model |
| Garage | Self-hosted | Good | Niche | Lightweight distributed object storage |
| SeaweedFS | Self-hosted | Advanced | Niche | Flexible, broad feature set |
| AWS S3 | External | Optional | Standard | Operationally simple, not self-hosted |
| Backblaze B2 | External | Optional | Good | S3-compatible hosted object storage |

---

## Hands-On Start

`minio-apps` follows the normal cluster path with a Helm chart. `minio-backup` is a Proxmox guest and has **no chart** — per the [Component Layout Convention](../../../../README.md#component-layout-convention), Proxmox guests get `docs` · `config` only.

Order for `minio-apps`:

1. Deploy on a Longhorn volume, single replica, and size the PVC deliberately small.
2. Create one bucket and one access key pair; keep the credentials in [Vault](../../security/secret-store).
3. Point one application at it and verify uploads survive a pod restart.
4. Drain the node it runs on and confirm it comes back elsewhere with its data.

Order for `minio-backup`, once disks exist:

1. Create the `tank/backups` dataset with its own quota.
2. Create the container and bind-mount that dataset as MinIO's data directory.
3. Point [Velero](../../backup/velero) at the endpoint and run one backup.
4. **Restore it into an empty namespace.** A backup nobody has restored is a hypothesis, not a backup.

---

## Deployment Links

```text
helm-charts/infrastructure/platform/storage/minio/     # chart — minio-apps only
infrastructure/platform/storage/minio/terraform/       # config — both instances
```

---

## Documentation

- [MinIO documentation](https://min.io/docs/minio/kubernetes/upstream/)
- [MinIO JavaScript SDK](https://min.io/docs/minio/linux/developers/javascript/minio-javascript.html)
- [MinIO Go SDK](https://min.io/docs/minio/linux/developers/go/minio-go.html)
- [Wikipedia: MinIO](https://en.wikipedia.org/wiki/MinIO)
- [Wikipedia: Object storage](https://en.wikipedia.org/wiki/Object_storage)
