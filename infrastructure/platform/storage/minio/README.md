# MinIO

[<- Back to Storage](../README.md)

MinIO provides S3-compatible object storage.

In this homelab, MinIO is the **chosen S3 target for cluster backups**, and it runs in a place that matters: as a **container on [`pve0`](../../../../setup/compute/proxmox-cluster) (`lxc`)**, not on the Kubernetes cluster. Its data directory is the `tank/backups` dataset of the [ZFS pool](../zfs-nas).

That placement is the entire point. A backup that lives inside the system it protects is not a backup — if [Velero](../../backup/velero) wrote its cluster backups to a MinIO running on the same cluster, a cluster failure would take the backups with it. Putting the bucket in the other world means the restore path survives the thing it restores.

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

## Where It Runs — And Why Not On The Cluster

| | |
|---|---|
| **Runs on** | `lxc` — a container on [`pve0`](../../../../setup/compute/proxmox-cluster) |
| **Data directory** | `tank/backups` on the [ZFS pool](../zfs-nas) |
| **Reached by** | Velero and Longhorn from the cluster, over the storage VLAN |

The obvious placement would be a MinIO Helm chart on the cluster, next to the workloads using it. That is exactly what must not happen for the backup role: **a backup stored inside the failure domain it protects is not a backup.** Wipe the cluster to rebuild it and the restore path goes with it.

Running MinIO on the Proxmox host puts one machine boundary and one filesystem boundary between the data and the thing being backed up — and it inherits ZFS snapshots for free, which means an accidental bucket deletion is also recoverable, not just a node failure.

The honest limit: `pve0` is still one box in one flat. It protects against cluster mistakes, not against fire or theft. That is what the `zfs send` copy off the machine is for, documented in [zfs-nas](../zfs-nas#operational-notes).

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

MinIO is currently `⚫ Inactive`. It becomes relevant at a specific moment: **before the first irreplaceable data exists**, because it is the target Velero writes to. In practice that means it is deployed together with the [ZFS pool](../zfs-nas), early in the Proxmox build and well before the cluster holds anything worth losing.

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

**Not a Helm chart.** MinIO runs as a Proxmox container, so there is no chart path for it — the [Component Layout Convention](../../../../README.md#component-layout-convention) gives `k8s` components a `chart` link and Proxmox guests a `config` link only. The guest definition will live with the other `pve0` guests once that section exists.

First evaluation order:

1. Create the `tank/backups` dataset with its own quota.
2. Create the container and bind-mount that dataset as MinIO's data directory.
3. Create one bucket and one access key pair; keep the credentials in [Vault](../../security/secret-store).
4. Point [Velero](../../backup/velero) at the endpoint and run one backup.
5. **Restore it into an empty namespace.** A backup nobody has restored is a hypothesis, not a backup.

---

## Configuration Link

```text
infrastructure/platform/storage/minio/terraform/
```

---

## Documentation

- [MinIO documentation](https://min.io/docs/minio/kubernetes/upstream/)
- [MinIO JavaScript SDK](https://min.io/docs/minio/linux/developers/javascript/minio-javascript.html)
- [MinIO Go SDK](https://min.io/docs/minio/linux/developers/go/minio-go.html)
- [Wikipedia: MinIO](https://en.wikipedia.org/wiki/MinIO)
- [Wikipedia: Object storage](https://en.wikipedia.org/wiki/Object_storage)
