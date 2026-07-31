# Sealed Secrets

[<- Back to Security](../README.md)

Sealed Secrets encrypts Kubernetes secrets so the encrypted form can be stored in Git. Only the controller inside the target cluster can decrypt them.

In this homelab, Sealed Secrets is a **documented alternative and is not planned**. [Vault](../secret-store) plus [External Secrets Operator](../external-secrets) covers the same problem more completely, and running both would mean two competing answers to "where does a secret live".

Sealed Secrets lets an operator take a Kubernetes Secret, encrypt it with a public key and commit the encrypted result to Git. The encrypted object is called a `SealedSecret`. Inside the cluster, the Sealed Secrets controller has the private key and can decrypt the value into a normal Kubernetes `Secret`.

This is useful when a team wants a GitOps workflow but does not yet have an external secret manager. Git contains encrypted secret material instead of plain text.

For beginners, the most important detail is key ownership. If the cluster's sealing private key is lost, the encrypted secrets in Git may no longer be usable. If the private key is leaked, the encrypted secrets are no longer safe.

---

## Why It Is Documented

Sealed Secrets is useful when there is no external secret manager yet, but GitOps should still avoid committing plain secret values.

It is often easier to start than a full vault system, which makes it attractive in homelabs and small clusters. It should still be treated as a deliberate tradeoff, not as a complete secret-management platform.

---

## Strengths

- Simple GitOps-friendly workflow.
- Does not require a separate secret backend.
- Encrypted manifests can be reviewed and stored in Git.
- Good bridge while the long-term Secret Store is still being evaluated.

---

## Weaknesses

- The sealing key becomes critical infrastructure and must be backed up.
- Rotation and secret lifecycle management are less rich than a real Secret Store.
- It is cluster-key-bound unless key management is planned carefully.
- It does not provide the same audit, dynamic credential or access-control model as Vault-style systems.

---

## Tradeoff

Sealed Secrets is simple, but the encrypted values are tied to the cluster key. Backup and restore of the sealing key becomes critical.

For this project, Sealed Secrets should be considered a fallback or bridge. The preferred long-term pattern is a real Secret Store plus External Secrets Operator where practical.

---

## Runtime Status

Sealed Secrets is `⚫ Inactive` and **not planned**. [Vault](../secret-store) with [External Secrets Operator](../external-secrets) is the chosen path.

**Why it lost, briefly:** Sealed Secrets solves exactly one problem — getting an encrypted value safely into Git. It has no rotation, no audit trail, no dynamic credentials and no access policies, and the secret is still pinned to one cluster's private key. Vault does all of that and more; adding Sealed Secrets next to it would only create a second place to look.

**When it would be the right choice:** a GitOps cluster with no external secret manager and no appetite to operate one. It is genuinely the simpler tool, and for a single-cluster setup that only needs a handful of static secrets, it is not a bad answer — just not this one.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/security/sealed-secrets/
```

---

## Learning Links

- [Sealed Secrets documentation](https://github.com/bitnami-labs/sealed-secrets)
- [Kubernetes Secrets documentation](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Wikipedia: Public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography)
- [Wikipedia: Secret sharing](https://en.wikipedia.org/wiki/Secret_sharing)
