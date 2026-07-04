# External Secrets Operator

[<- Back to Security](../README.md)

External Secrets Operator syncs secrets from an external secret manager into Kubernetes `Secret` resources.

It separates secret values from Git-managed Kubernetes manifests.

Many Helm charts and Kubernetes applications expect credentials to appear as Kubernetes `Secret` objects. That creates a GitOps problem: the chart values and manifests belong in Git, but the secret values must not be stored in Git as plain text.

External Secrets Operator solves this by making Kubernetes reference an external secret backend. The real value stays in a system such as Vault, OpenBao, Infisical, 1Password, Bitwarden or a cloud secret manager. External Secrets Operator reads the approved value and creates or updates the Kubernetes `Secret` inside the cluster.

For beginners, the key point is that External Secrets Operator is a bridge. It is not the source of truth for the secret. The external secret manager is the source of truth.

---

## Why It Fits

GitOps needs a clean answer for secrets. External Secrets Operator allows deployment configuration to stay in Git while secret material stays in a dedicated backend.

This pattern is especially useful for Helm charts that are not written to call a secret backend directly. The chart can keep using a normal Kubernetes `Secret`, while the sensitive value is managed somewhere safer.

---

## Used For

- syncing database passwords into Kubernetes Secrets
- giving Helm charts credentials without committing values to Git
- rotating secrets in a backend and letting Kubernetes receive updates
- separating secret ownership from application deployment files
- integrating GitOps with a Secret Store

---

## Strengths

- Strong fit for GitOps because manifests can reference secrets without containing values.
- Works with many secret backends.
- Lets existing Kubernetes workloads keep using standard `Secret` objects.
- Centralizes secret source-of-truth decisions outside application charts.
- Supports clearer separation between deploy permissions and secret management permissions.

---

## Weaknesses

- The cluster still receives Kubernetes Secrets, so Kubernetes secret security still matters.
- Backend authentication and access policy must be designed carefully.
- It adds another controller that must be monitored.
- It does not replace human password management or application authorization.
- A broken secret backend can affect application startup and rotation.

---

## Possible Backends

- 1Password
- Bitwarden Secrets Manager
- HashiCorp Vault
- OpenBao
- Infisical
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

---

## Learning Links

- [External Secrets Operator documentation](https://external-secrets.io/)
- [Kubernetes Secrets documentation](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Wikipedia: Secret management](https://en.wikipedia.org/wiki/Secrets_management)
- [Wikipedia: Principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)
