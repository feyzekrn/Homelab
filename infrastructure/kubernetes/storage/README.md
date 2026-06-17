# Kubernetes Storage

[<- Back to Kubernetes](../README.md)

Storage covers persistent data for workloads. In Kubernetes this usually means StorageClasses, PersistentVolumeClaims, backup plans and restore testing.

---

## Components

| Component | Status | Location | Recommendation | Role | Documentation |
|---|---|---|---|---|---|
| Longhorn | ⚫ Inactive | Self-hosted | Homelab standard | Distributed block storage | [longhorn](./longhorn) |
| MinIO | ⚫ Inactive | Self-hosted | Homelab S3 standard | S3-compatible object storage | [minio](./minio) |

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
