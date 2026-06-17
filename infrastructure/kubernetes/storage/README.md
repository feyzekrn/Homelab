# Kubernetes Storage

[<- Back to Kubernetes](../README.md)

Storage covers persistent data for workloads. In Kubernetes this usually means StorageClasses, PersistentVolumeClaims, backup plans and restore testing.

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

| Path | Status | Location | Recommendation | Role |
|---|---|---|---|---|
| [`./longhorn`](./longhorn) | ⚫ Inactive | Self-hosted | Homelab standard | Distributed block storage |
| [`./minio`](./minio) | ⚫ Inactive | Self-hosted | Homelab S3 standard | S3-compatible object storage |

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
