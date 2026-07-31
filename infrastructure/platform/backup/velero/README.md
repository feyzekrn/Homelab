# Velero

[<- Back to Backup](../README.md)

Velero backs up and restores Kubernetes resources and persistent volume data (`k8s`).

It is useful for disaster recovery, cluster migration and testing rebuild workflows.

**It covers the cluster only.** The Proxmox world has its own tooling — `vzdump` now, [Proxmox Backup Server](../proxmox-backup-server) later — because containers and VMs are not Kubernetes objects. Two worlds, two backup tools, documented together in the [backup overview](../README.md).

Velero is a Kubernetes backup tool. It can save Kubernetes API resources such as Deployments, Services, Ingresses, ConfigMaps and custom resources. Depending on the storage integration, it can also coordinate persistent volume backups.

Velero is not a magic full-system backup. It must be configured with a backup location, usually object storage such as S3 or MinIO. It also needs a clear decision about volume backups and database backups. For serious databases, a database-native backup is often still required because crash-consistent volume copies are not always enough.

---

## Why It Fits

This project is explicitly about breaking and rebuilding infrastructure. Velero provides a structured way to test whether the cluster can recover from mistakes, node loss or a full rebuild.

It also teaches an important production habit: write the restore procedure before relying on the backup. A Velero backup is only valuable if the project can explain where it is stored, how credentials are recovered, how namespaces are restored and which workloads need extra application-level recovery.

---

## Prerequisites

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../kubernetes/cilium) | It runs as pods |
| [Longhorn](../../storage/longhorn) | The volumes being backed up, and the CSI snapshot integration |
| **[MinIO (backup)](../../storage/minio) on `pve0`** | The S3 target — and it must be the `lxc` instance, not the cluster one |
| Disks in `pve0` → [ZFS pool](../../storage/zfs-nas) | MinIO's backup instance has nowhere to write without them |
| [Vault](../../security/secret-store) | S3 credentials do not belong in a values file |

**The target must not be the cluster.** Velero writing to a MinIO running on the same cluster is a backup stored inside the failure domain it protects — wipe the cluster and the restore path goes with it. This is why [MinIO is deployed twice](../../storage/minio#how-each-instance-is-built), and pointing Velero at the wrong one silently produces useless backups.

Consequence worth stating: **the whole backup chain is currently blocked on two hard drives.** Until `pve0` has disks, the cluster has no valid backup target, and anything deployed before then runs without a restore path.

---

## Used For

- namespace backups
- Kubernetes resource backups
- persistent volume backup integration
- restore testing
- migration experiments

---

## Strengths

- Kubernetes-aware backup and restore workflow.
- Can back up namespaces and selected resources instead of only whole disks.
- Supports common object-storage backup targets.
- Useful for cluster migration and disaster-recovery drills.
- Fits GitOps well when the boundary between Git-managed configuration and runtime data is documented.

---

## Weaknesses

- It does not replace database-native backups for important relational or document databases.
- Volume backup support depends on the storage provider and plugins.
- Restoring custom resources can be tricky if CRDs and operators are not restored in the right order.
- Backup credentials and backup storage must survive the same failure being tested.
- Poor label/namespace discipline can make selective restores confusing.

---

## Alternatives

| Alternative | Notes |
|---|---|
| Longhorn backups | Good for volume-level backups |
| Database-native backups | Required for serious database recovery |
| GitOps only | Restores manifests, not runtime data |

---

## Restore Drill Example

1. Deploy a small test application with a PVC.
2. Write test data into the application.
3. Create a Velero backup of the namespace.
4. Delete the namespace.
5. Restore the namespace from Velero.
6. Verify the application starts and the data is still present.
7. Document every manual step that was required.

---

## Runtime Status

Velero is currently `⚫ Inactive`. The timing rule is simple and worth holding to: **it must run before the first irreplaceable data exists on the cluster**, not after. Retrofitting backups onto data that already matters means the gap was real for however long it took.

In practice it is blocked by the same hardware as everything else in the backup chain — see the prerequisites above.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/backup/velero/
```

---

## Learning Links

- [Velero documentation](https://velero.io/docs/)
- [Wikipedia: Backup](https://en.wikipedia.org/wiki/Backup)
- [Wikipedia: Disaster recovery](https://en.wikipedia.org/wiki/Disaster_recovery)
- [Wikipedia: Object storage](https://en.wikipedia.org/wiki/Object_storage)
