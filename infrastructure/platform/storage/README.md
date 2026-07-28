# Kubernetes Storage

[<- Back to Platform](../README.md)

Storage covers persistent data for workloads. In Kubernetes this usually means StorageClasses, PersistentVolumeClaims, backup plans and restore testing.

Containers are temporary. Kubernetes may stop a pod, move it to another node or replace it during an update. That is fine for stateless applications, but it is not fine for data that must survive.

Kubernetes storage gives pods a way to use persistent data. A workload asks for storage through a PersistentVolumeClaim, Kubernetes binds that request to a PersistentVolume and a StorageClass defines how the storage is provisioned.

There are different storage types. Block storage behaves like a disk attached to a workload and is common for databases. Object storage behaves like buckets accessed through an API and is common for backups, uploads and S3-compatible applications. This directory documents both because they solve different problems.

---

## Why This Matters

Containers are disposable, but data is not. Kubernetes can restart pods on different nodes, reschedule workloads and replace containers, but stateful applications need their data to survive those changes.

In a homelab, storage is where the cluster becomes real. Databases, file uploads, media metadata, dashboards and backups all depend on storage behavior. It is also where failures become visible quickly: node reboots, disk pressure, broken mounts and restore mistakes are hard to hide.

In companies, storage is treated as a reliability layer. Teams care about performance, replication, encryption, backup policies, restore time, data ownership and compliance. The homelab version should stay smaller, but it should teach the same operational instincts.

---

## What You Can Do With It

- provide persistent volumes for databases
- store uploaded files and application data
- create S3-compatible buckets with MinIO
- test node failure and volume recovery
- practice backup and restore workflows
- separate block storage from object storage
- document which data is important and how it is recovered

---

## Components

| Name | Path | Status | Runs on | Idle RAM | Recommendation | Role |
|---|---|---|---|---|---|---|
| Longhorn | [docs](./longhorn) · [chart](../../../helm-charts/infrastructure/platform/storage/longhorn) · [config](./longhorn/terraform) | ⚫ Inactive | k8s | ~0.3–0.5 GB / node | Chosen block storage | Distributed block storage for the cluster |
| ZFS + shares 🗄️ NAS | [docs](./zfs-nas) · [config](./zfs-nas/terraform) | ⚫ Inactive | lxc | ~0.1 GB service + ZFS ARC | Chosen NAS approach | ZFS pool on the host, published through a share container |
| MinIO | [docs](./minio) · [config](./minio/terraform) | ⚫ Inactive | lxc | ~0.2–0.5 GB | Chosen S3 target | S3-compatible object storage for backups |
| TrueNAS SCALE 🗄️ NAS | [docs](./truenas) | ⚫ Inactive | — | ~8–16 GB | Documented alternative | Full NAS operating system as a VM |
| OpenMediaVault 🗄️ NAS | [docs](./openmediavault) | ⚫ Inactive | — | ~1–2 GB | Documented alternative | Lightweight NAS distribution on Debian |

Rows marked 🗄️ **NAS** are competing answers to the same question — where the household's files live. The [ZFS-on-host approach](./zfs-nas) is chosen because it keeps datasets bind-mountable into the app containers instead of forcing every access through the network.

---

## Block Storage vs Object Storage

| Type | Looks like | Best for | Example |
|---|---|---|---|
| Block storage | A mounted disk or volume | Databases, app data directories, stateful pods | Longhorn volume for PostgreSQL |
| Object storage | Buckets and objects through an API | Backups, uploads, artifacts, S3-compatible apps | MinIO bucket for Velero backups |
| File storage | Shared filesystem path | Shared media or legacy apps | NFS or SMB share |

---

## Baseline Choice

Use Longhorn as the first storage layer. It is approachable, Kubernetes-native and exposes important concepts such as replicas, volume attachment, node failure and backup targets.

Object storage with MinIO is useful later for backups, artifacts and S3-compatible application testing. It is the first S3-equivalent to evaluate for this homelab.

---

## Operational Rule

Databases make storage problems visible quickly. Before putting real data into PostgreSQL, MySQL or MongoDB, test:

- node reboot
- pod rescheduling
- volume detach and attach
- backup
- restore
- disk pressure behavior

---

## Learning Links

- [Kubernetes storage documentation](https://kubernetes.io/docs/concepts/storage/)
- [Wikipedia: Computer data storage](https://en.wikipedia.org/wiki/Computer_data_storage)
- [Wikipedia: Block-level storage](https://en.wikipedia.org/wiki/Block-level_storage)
- [Wikipedia: Object storage](https://en.wikipedia.org/wiki/Object_storage)
