# External Secrets Operator

[<- Back to Security](../README.md)

External Secrets Operator syncs secrets from an external secret manager into Kubernetes `Secret` resources.

It separates secret values from Git-managed Kubernetes manifests.

---

## Why It Fits

GitOps needs a clean answer for secrets. External Secrets Operator allows deployment configuration to stay in Git while secret material stays in a dedicated backend.

---

## Possible Backends

- 1Password
- Bitwarden Secrets Manager
- HashiCorp Vault
- AWS Secrets Manager
- Kubernetes cluster secret store for early experiments

---

## Runtime Status

External Secrets Operator is currently `⚫ Inactive`. It is a core candidate once GitOps is introduced and secrets need to be managed without committing plain values to Git.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/security/external-secrets/
```
