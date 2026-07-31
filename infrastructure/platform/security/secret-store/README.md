# Secret Store

[<- Back to Security](../README.md)

A Secret Store is the source of truth for sensitive values such as API tokens, database passwords, service credentials, SSH keys, account recovery material and integration secrets.

**The chosen system is HashiCorp Vault** (`k8s`), with [OpenBao](../openbao) documented as the drop-in alternative should the licence become a problem.

This is different from Kubernetes `Secret` objects. Kubernetes secrets are a delivery mechanism inside the cluster. A real Secret Store manages secrets, permissions, audit trails, rotation and programmatic access.

It is also different from a **password manager**. Vault holds *application* secrets that workloads read at runtime; [Vaultwarden](../password-manager/bitwarden) holds *human* secrets that people type. Collapsing the two mixes very different threat models — the boundary is explained in [password-manager](../password-manager).

---

## Project Goal

The goal is a modern developer-friendly secret system that can serve two worlds:

- private or human-managed credentials, similar to a password manager
- application and infrastructure secrets, consumed programmatically by services

Applications should not hard-code credentials and should not know the final backend. They should access secrets through an abstraction such as Dapr where possible.

---

## Recommended Direction

Use a real Secret Store as the source of truth, then expose secrets through narrow access paths:

- humans manage credentials through a UI, CLI or browser/mobile password workflow
- services authenticate with workload identity, service tokens or Kubernetes identity
- applications read only the secrets they are allowed to access
- Dapr acts as a runtime abstraction for app code where supported
- External Secrets Operator syncs selected secrets into Kubernetes only when a Kubernetes `Secret` is actually needed

This keeps app code clean while preserving a central access-control and audit model.

---

## Dapr Access Model

Dapr has a Secrets API. Application code asks Dapr for a secret by store name and key. Dapr talks to the configured backend.

Conceptually:

```text
Application code
  -> Dapr sidecar
    -> Secret Store component
      -> Secret backend
```

Example use cases:

- a Go API reads a database password at startup
- a worker retrieves an external API token before calling a hardware service
- a dashboard backend reads OAuth client credentials
- a mobile companion backend reads push notification credentials

The app should request logical secret names, not backend-specific paths. That keeps the code portable if the backend changes later.

---

## Prerequisites

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../kubernetes/cilium) | It runs as pods |
| [Longhorn](../../storage/longhorn) | Vault's storage backend must persist — losing it loses every secret |
| An **unseal strategy decided up front** | Vault starts sealed after every restart; see below |
| [External Secrets Operator](../external-secrets) | The bridge into Kubernetes `Secret` objects for charts that expect them |
| A backup path | The one component where losing state is unrecoverable rather than inconvenient |

### The unseal problem — decide before deploying

Vault encrypts its storage and starts **sealed** after every restart. Until it is unsealed it answers nothing, which means a node reboot at 03:00 can silently break every workload that reads a secret at startup.

Three options, in increasing order of comfort and decreasing order of purity:

| Approach | Trade |
|---|---|
| Manual unseal | Most secure, and genuinely painful — every restart needs a human with key shares |
| Auto-unseal via a cloud KMS | Reliable, but puts the root of trust in a provider this project is trying to leave |
| Transit auto-unseal from a second Vault | Self-hosted and automatic; the second instance becomes the thing that must not die |

**This is not a detail to postpone.** A homelab Vault that requires manual unseal after every power event will be worked around within a month, and the workaround is always worse than the original problem.

---

## Why Vault Was Chosen

| System | Why not |
|---|---|
| **HashiCorp Vault** | **Chosen** — the industry standard, and the one whose concepts transfer directly to professional work |
| [OpenBao](../openbao) | Near drop-in fork under the Linux Foundation; the documented escape hatch if the BUSL licence becomes a problem |
| Infisical | Better developer UX, much smaller ecosystem and a shorter track record |
| 1Password / Bitwarden Secrets Manager | Strong for human secrets; [Vaultwarden](../password-manager/bitwarden) already covers that half |
| Google Secret Manager | Managed and reliable, but the opposite of the point of this homelab |

The deciding factor is **transferable knowledge**. Vault's model — engines, policies, roles, dynamic credentials, leases — is what appears in real infrastructure, and learning it here means learning it once. The licence change to BUSL is a genuine concern, which is exactly why OpenBao is documented rather than dismissed: it is API-compatible, so the migration path exists if it is ever needed.

**The learning target worth aiming at is dynamic credentials.** Vault can issue a PostgreSQL user that exists for one hour and is then revoked automatically. A static password copied into a values file is what most homelabs do; short-lived credentials issued on demand are what makes the tool worth its operational weight.

---

## PAM Note

In this context, PAM means Privileged Access Management: controlled access to sensitive accounts, credentials and privileged actions.

That is different from Linux PAM, the Pluggable Authentication Modules system used by Linux for login and authentication flows.

Privileged Access Management becomes relevant if the homelab stores shared admin accounts, hardware-management credentials, recovery accounts or other high-impact secrets. The system should make it clear who accessed which credential, when and why.

---

## The Split This Project Uses

The question "one system for everything, or two?" is settled here in favour of two, each doing what it is good at:

| | Holds | System | Runs on |
|---|---|---|---|
| **Application secrets** | DB passwords, API tokens, service credentials | Vault | `k8s` |
| **Human secrets** | Family logins, recovery codes, break-glass accounts | [Vaultwarden](../password-manager/bitwarden) | `lxc` on `pve0` |

The placement is not accidental. Vaultwarden holds the [break-glass credentials](../rights-management/keycloak#break-glass-access) for the cluster — which means it must be reachable when the cluster is not. A password manager that lives inside the system it holds the recovery keys for is a locked door with the key inside.

---

## Private Passwords And App Secrets

Do not give applications broad access to personal password vaults.

Instead:

- keep personal accounts in a human-friendly password manager or dedicated vault project
- create separate service accounts for applications
- expose only selected secrets through policy
- prefer short-lived credentials where possible
- audit every application secret read if the backend supports it

This allows personal accounts and application secrets to be linked operationally without giving every service access to everything.

---

## Access Patterns

| Pattern | Use case | Notes |
|---|---|---|
| Dapr Secrets API | Application reads secrets at runtime | Best abstraction for app code if backend is supported |
| External Secrets Operator | Kubernetes object needs a `Secret` | Good for charts that expect Kubernetes secrets |
| Direct SDK/API | Service talks directly to secret backend | Powerful, but couples app code to one provider |
| CLI-injected env files | Local development | Useful for dev, not a production pattern |

---

## Runtime Status

Vault is currently `⚫ Inactive`. It must exist **before the first application needs a credential**, because the alternative — a password pasted into a values file "just for now" — is the thing that never gets cleaned up and ends up in Git history.

In the build order it comes after [Longhorn](../../storage/longhorn) and alongside [External Secrets](../external-secrets), and before [cert-manager](../../ingress/cert-manager), which needs the Cloudflare API token to come from somewhere.

**Back it up before putting anything in it.** Every other component in this catalog can be rebuilt from documentation. A lost Vault is lost secrets.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/security/secret-store/
```

---

## References

- [Dapr supported secret stores](https://docs.dapr.io/reference/components-reference/supported-secret-stores/)
- [Infisical documentation](https://infisical.com/docs)
- [OpenBao documentation](https://openbao.org/docs/)
- [Wikipedia: Secret management](https://en.wikipedia.org/wiki/Secrets_management)
- [Wikipedia: Password manager](https://en.wikipedia.org/wiki/Password_manager)
- [Wikipedia: Privileged access management](https://en.wikipedia.org/wiki/Privileged_access_management)
- [Wikipedia: Principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)
