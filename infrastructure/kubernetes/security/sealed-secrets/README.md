# Sealed Secrets

[<- Back to Security](../README.md)

Sealed Secrets encrypts Kubernetes secrets so the encrypted form can be stored in Git.

Only the controller inside the target cluster can decrypt them.

---

## Why It Is Documented

Sealed Secrets is useful when there is no external secret manager yet, but GitOps should still avoid committing plain secret values.

---

## Tradeoff

Sealed Secrets is simple, but the encrypted values are tied to the cluster key. Backup and restore of the sealing key becomes critical.

---

## Runtime Status

Sealed Secrets is currently `⚫ Inactive`. Compare it against External Secrets Operator before choosing a long-term secret workflow.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/security/sealed-secrets/
```
