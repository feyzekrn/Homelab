# Secret Store

[<- Back to Security](../README.md)

A Secret Store is the source of truth for sensitive values such as API tokens, database passwords, service credentials, SSH keys, account recovery material and integration secrets.

This is different from Kubernetes `Secret` objects. Kubernetes secrets are a delivery mechanism inside the cluster. A real Secret Store manages secrets, permissions, audit trails, rotation and programmatic access.

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

## Candidate Systems

| System | Best fit | Notes |
|---|---|---|
| Infisical | Modern developer-friendly secrets platform, self-hosting, app secrets, human workflows, PAM direction | Strong candidate if the goal is a polished password-manager-like developer experience |
| OpenBao | Open-source Vault-style secret management | Strong candidate for Kubernetes-native and Dapr-compatible secret backend experiments |
| HashiCorp Vault | Mature secrets engine and dynamic credentials | Very capable, but licensing and operational model should be considered |
| 1Password Secrets Automation | Excellent human password manager with developer automation | Great if personal password manager integration matters more than self-hosting |
| Bitwarden Secrets Manager | Password manager ecosystem with machine secrets | Good bridge between human and service secrets |
| Google Secret Manager | Managed cloud secret backend | Useful if cloud integration is acceptable, less self-hosted |
| Apple Passwords / iCloud Keychain | Human password management | Good personal UX, but not a practical runtime backend for Kubernetes apps |
| Google Password Manager | Human password management | Useful for personal accounts, but Google Secret Manager is the app-facing backend option |

---

## PAM Note

In this context, PAM means Privileged Access Management: controlled access to sensitive accounts, credentials and privileged actions.

That is different from Linux PAM, the Pluggable Authentication Modules system used by Linux for login and authentication flows.

Privileged Access Management becomes relevant if the homelab stores shared admin accounts, hardware-management credentials, recovery accounts or other high-impact secrets. The system should make it clear who accessed which credential, when and why.

---

## Comparison Notes

Infisical is attractive because it feels closer to a modern developer platform and includes human-friendly secret workflows. OpenBao and Vault are stronger as infrastructure-grade secret engines and map well to Kubernetes and Dapr-style runtime access. 1Password and Bitwarden are strong when private human passwords and shared accounts are central. Apple Passwords and Google Password Manager are useful for personal accounts, but they are not the same as a programmable application Secret Store.

For this homelab, a good research path is:

1. Evaluate Infisical for developer experience, private account workflows and PAM-like capabilities.
2. Evaluate OpenBao for Dapr-backed runtime secret access.
3. Decide whether one system can cover both, or whether personal passwords stay in a password manager while application secrets live in OpenBao or Infisical.

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

Secret Store is currently `⚫ Inactive`. It should become a core security service before applications start depending on private API keys, database passwords or shared accounts.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/security/secret-store/
```

---

## References

- [Dapr supported secret stores](https://docs.dapr.io/reference/components-reference/supported-secret-stores/)
- [Infisical documentation](https://infisical.com/docs)
- [OpenBao documentation](https://openbao.org/docs/)
