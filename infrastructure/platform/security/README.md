# Security

[<- Back to Platform](../README.md)

This directory documents cluster security building blocks that are shared across services.

The first focus is secrets management and access control. Later this area can also include policy engines, image scanning and runtime security.

Security in this project is about controlling sensitive access. That includes human login, application credentials, service accounts, Kubernetes permissions, secret storage and the rules that decide who may do what.

For beginners, it helps to separate three ideas:

- Authentication asks: who are you?
- Authorization asks: what are you allowed to do?
- Secret management asks: how are sensitive values stored, accessed, rotated and audited?

Kubernetes has built-in security features such as RBAC and `Secret` objects, but those are not the whole solution. A real platform also needs identity, least privilege, safe GitOps secret workflows and a clear boundary between personal passwords and application secrets.

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

| Name | Path | Idle RAM | Role |
|---|---|---|---|
| Secret Store | [docs](./secret-store) · [chart](../../../helm-charts/infrastructure/platform/security/secret-store) · [config](./secret-store/terraform) | ~0.2–0.5 GB | Runtime secret access for applications and infrastructure integrations |
| External Secrets Operator | [docs](./external-secrets) · [chart](../../../helm-charts/infrastructure/platform/security/external-secrets) · [config](./external-secrets/terraform) | ~50–100 MB | Syncs secrets from an external secret backend into Kubernetes |
| Sealed Secrets | [docs](./sealed-secrets) · [chart](../../../helm-charts/infrastructure/platform/security/sealed-secrets) · [config](./sealed-secrets/terraform) | ~50 MB | Encrypts Kubernetes secrets safely for Git storage |
| Rights Management | [docs](./rights-management) | — | Identity, permissions and application authorization model (category) |
| Password Manager | [docs](./password-manager) | — | Human password vault for the family (category, chosen: Bitwarden/Vaultwarden) |

---

## Recommendation

Start simple while learning. Do not commit plain Kubernetes `Secret` values to Git.

For a long-term GitOps setup, prefer a real Secret Store as the source of truth. External Secrets Operator can sync selected values into Kubernetes, while Dapr can let applications read secrets at runtime through an abstraction layer.

Use Sealed Secrets only when the goal is encrypted secrets directly in Git without running a separate vault system.

---

## Important Distinction

There are three related but different problems:

- Human password management: private accounts, shared accounts, recovery keys and login credentials — covered by [`./password-manager`](./password-manager).
- Runtime application secrets: API keys, database passwords, tokens and service credentials used by applications — covered by [`./secret-store`](./secret-store) and [`./external-secrets`](./external-secrets).
- Authorization: deciding which user, service or workload is allowed to read or use which secret — covered by [`./rights-management`](./rights-management).

The project should connect these worlds carefully, not collapse them into one unrestricted store.

---

## Typical Security Flow

1. A human logs in through an identity provider such as Keycloak.
2. The application receives a token that proves who the user is.
3. The application checks roles or permissions before allowing an action.
4. The application reads only the runtime secrets it is allowed to use.
5. The Secret Store or External Secrets workflow provides credentials without putting plain values in Git.
6. Audit logs and documentation explain what happened later.

---

## Learning Links

- [Wikipedia: Authentication](https://en.wikipedia.org/wiki/Authentication)
- [Wikipedia: Authorization](https://en.wikipedia.org/wiki/Authorization)
- [Wikipedia: Principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)
- [Wikipedia: Single sign-on](https://en.wikipedia.org/wiki/Single_sign-on)
- [Kubernetes Secrets documentation](https://kubernetes.io/docs/concepts/configuration/secret/)
