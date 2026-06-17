# Rights Management

[<- Back to Security](../README.md)

Rights Management describes how users, services and workloads receive permissions.

For this homelab, it should eventually answer questions like:

- Which app may read which secret?
- Which user may trigger hardware power actions?
- Which service may publish to NATS or Kafka?
- Which dashboard user may modify cluster settings?
- Which automation job may access private account credentials?

---

## Scope

This is broader than Kubernetes RBAC. Kubernetes RBAC controls access to Kubernetes resources. Application authorization controls what users and services can do inside the applications themselves.

Both are needed.

---

## Candidate Systems

| System | Best fit | Notes |
|---|---|---|
| Keycloak | Identity provider, OIDC, OAuth2, SSO, realm and client management | Strong default if self-hosted identity is needed |
| Authentik | Modern self-hosted identity provider | Good UX and homelab-friendly |
| Zitadel | Identity provider with strong modern cloud-native design | Good candidate for OIDC/OAuth2 learning |
| OpenFGA | Relationship-based authorization | Good for fine-grained app permissions |
| SpiceDB | Zanzibar-style authorization system | Powerful for complex permission graphs |
| Casbin | Authorization library embedded in apps | Lightweight but less centralized |

---

## Recommended Direction

Start with identity first, then authorization:

1. Use an identity provider such as Keycloak, Authentik or Zitadel for login, OIDC and service identities.
2. Use Kubernetes RBAC for cluster-level permissions.
3. Evaluate OpenFGA or SpiceDB if application permissions become complex.
4. Build a custom rights-management service only if the generic tools do not fit the desired model.

---

## Secret Store Integration

Rights Management should eventually define policies like:

- dashboard backend can read dashboard OAuth credentials
- hardware automation service can read Intel vPro credentials
- CI/CD service can read package publishing tokens
- user account `admin` can rotate shared secrets
- mobile companion backend cannot read database root passwords

The actual secret backend should enforce the final access decision where possible. Application-level authorization can additionally control which user actions are allowed.

---

## Application Examples

- A user logs into the admin dashboard through OIDC.
- The dashboard checks whether the user may restart a node.
- The node-control service reads only its own hardware credentials from the Secret Store.
- A CI service can publish npm packages but cannot read database passwords.
- A mobile app can view cluster health but cannot rotate credentials.

---

## Runtime Status

Rights Management is currently `⚫ Inactive`. Keep it documented while the application model is still forming. Revisit once the first dashboard, API or automation service needs real user roles.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/security/rights-management/
```

---

## References

- [OpenFGA documentation](https://openfga.dev/docs)
- [SpiceDB documentation](https://authzed.com/docs/spicedb)
