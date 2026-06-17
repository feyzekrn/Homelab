# Security

[<- Back to Kubernetes](../README.md)

This directory documents cluster security building blocks that are shared across services.

The first focus is secrets management and access control. Later this area can also include policy engines, image scanning and runtime security.

---

## Why This Matters

Security is the layer that decides who can access what, which services are allowed to talk to sensitive systems and how secrets are handled. Without this, a homelab quickly turns into a collection of passwords in environment files, admin tokens in notes and services with more permissions than they need.

In a homelab, the goal is not enterprise bureaucracy. The goal is to build good habits early: no plain secrets in Git, separate personal passwords from application secrets, use service identities, and make privileged access intentional.

In companies, these same ideas become formal controls: identity providers, least privilege, audit trails, secret rotation, compliance requirements and security reviews. This repository documents the smaller but still realistic version.

---

## What You Can Do With It

- centralize application secrets
- give apps runtime secret access through Dapr
- sync selected secrets into Kubernetes
- protect dashboards and tools with SSO
- model user roles such as admin, operator and viewer
- prepare future policy and authorization work
- avoid committing credentials into Git

---

## Components

| Path | Role |
|---|---|
| [`./secret-store`](./secret-store) | Runtime secret access for applications and infrastructure integrations |
| [`./external-secrets`](./external-secrets) | Syncs secrets from an external secret backend into Kubernetes |
| [`./sealed-secrets`](./sealed-secrets) | Encrypts Kubernetes secrets safely for Git storage |
| [`./rights-management`](./rights-management) | Identity, permissions and application authorization model |

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
