# Velero

[<- Back to Backup](../README.md)

Velero backs up and restores Kubernetes resources and persistent volume data.

It is useful for disaster recovery, cluster migration and testing rebuild workflows.

---

## Why It Fits

This project is explicitly about breaking and rebuilding infrastructure. Velero provides a structured way to test whether the cluster can recover from mistakes, node loss or a full rebuild.

---

## Used For

- namespace backups
- Kubernetes resource backups
- persistent volume backup integration
- restore testing
- migration experiments

---

## Alternatives

| Alternative | Notes |
|---|---|
| Longhorn backups | Good for volume-level backups |
| Database-native backups | Required for serious database recovery |
| GitOps only | Restores manifests, not runtime data |

---

## Runtime Status

Velero is currently `⚫ Inactive`. It is optional at the start, but should become a core candidate before important data is stored.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/backup/velero/
```
