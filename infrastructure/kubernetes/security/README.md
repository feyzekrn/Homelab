# Security

[<- Back to Kubernetes](../README.md)

This directory documents cluster security building blocks that are shared across services.

The first focus is secrets management and access control. Later this area can also include policy engines, image scanning and runtime security.

---

## Components

| Component | Role | Documentation |
|---|---|---|
| Secret Store | Runtime secret access for applications and infrastructure integrations | [secret-store](./secret-store) |
| External Secrets Operator | Syncs secrets from an external secret backend into Kubernetes | [external-secrets](./external-secrets) |
| Sealed Secrets | Encrypts Kubernetes secrets safely for Git storage | [sealed-secrets](./sealed-secrets) |
| Rights Management | Identity, permissions and application authorization model | [rights-management](./rights-management) |

---

## Recommendation

Start simple while learning. Do not commit plain Kubernetes `Secret` values to Git.

For a long-term GitOps setup, prefer a real Secret Store as the source of truth. External Secrets Operator can sync selected values into Kubernetes, while Dapr can let applications read secrets at runtime through an abstraction layer.

Use Sealed Secrets only when the goal is encrypted secrets directly in Git without running a separate vault system.

---

## Important Distinction

There are three related but different problems:

- Human password management: private accounts, shared accounts, recovery keys and login credentials.
- Runtime application secrets: API keys, database passwords, tokens and service credentials used by applications.
- Authorization: deciding which user, service or workload is allowed to read or use which secret.

The project should connect these worlds carefully, not collapse them into one unrestricted store.
