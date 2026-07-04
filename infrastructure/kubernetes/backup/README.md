# Backup

[<- Back to Kubernetes](../README.md)

Backups are not optional once the cluster stores useful data.

This directory documents backup tooling, restore tests and disaster recovery decisions.

A backup is a copy of data that can be used after deletion, corruption, hardware failure or a bad deployment. In Kubernetes, "backup" is not one single thing. The cluster contains manifests, runtime resources, persistent volumes, database data, object buckets, secrets and sometimes external systems.

GitOps can recreate many Kubernetes manifests, but GitOps does not restore uploaded files, database rows, Redis state, MinIO buckets or Longhorn volume contents. That is why backup planning must describe both configuration recovery and data recovery.

The most important beginner rule is simple: a backup that has never been restored is not proven. The restore process is part of the backup design.

---

## Why This Matters

A backup strategy is only real if restore has been tested. Kubernetes resources, persistent volumes, database dumps and object storage may all need different recovery workflows.

In a homelab, backup work teaches what data is actually important and how painful a rebuild would be. In companies, backup and disaster recovery are tied to recovery-time objectives, recovery-point objectives, compliance and business continuity.

---

## What You Can Do With It

- back up Kubernetes resources
- back up persistent volumes
- test namespace restore
- practice disaster recovery after a cluster rebuild
- separate GitOps-restored manifests from runtime data
- document which systems need database-native backups

---

## What Needs Different Backup Thinking

| Data type | Example | Likely recovery path |
|---|---|---|
| Git-managed manifests | HelmRelease, Kustomization, Ingress | Restore from Git through Flux or Argo CD |
| Kubernetes runtime resources | Namespaces, ConfigMaps, CRDs | Velero or GitOps, depending on ownership |
| Persistent volumes | Database volume, Nextcloud data | Longhorn backup, Velero volume backup or storage-native backup |
| Databases | PostgreSQL, MySQL, MongoDB | Database-native dump or operator-managed backup |
| Object storage | MinIO buckets | Bucket replication, object backup or storage backend backup |
| Secrets | Secret Store, sealing keys, tokens | Secret backend export/backup and key escrow |

---

## Beginner Concepts

- RPO means Recovery Point Objective: how much data loss is acceptable.
- RTO means Recovery Time Objective: how long recovery may take.
- Disaster recovery means restoring service after a major failure, not just undeleting one file.
- Versioned backups protect against accidental deletion and some corruption cases.
- Off-cluster backups matter because a cluster-wide failure can destroy local copies.

---

## Components

| Path | Role |
|---|---|
| [`./velero`](./velero) | Kubernetes resource and volume backup orchestration |

---

## Rule

A backup that has never been restored is only a hope. Every important backup workflow should have a documented restore test.

---

## Learning Links

- [Wikipedia: Backup](https://en.wikipedia.org/wiki/Backup)
- [Wikipedia: Disaster recovery](https://en.wikipedia.org/wiki/Disaster_recovery)
- [Wikipedia: Recovery point objective](https://en.wikipedia.org/wiki/Recovery_point_objective)
- [Velero documentation](https://velero.io/docs/)
