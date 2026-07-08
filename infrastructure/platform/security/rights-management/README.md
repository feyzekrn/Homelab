# Rights Management

[<- Back to Security](../README.md)

Rights Management describes how users, services and workloads receive permissions.

For this homelab, it should eventually answer questions like:

- Which app may read which secret?
- Which user may trigger hardware power actions?
- Which service may publish to NATS or Kafka?
- Which dashboard user may modify cluster settings?
- Which automation job may access private account credentials?

Rights Management is the answer to "who may do what?" Authentication can prove that a user is Alice, but authorization decides whether Alice may restart a node, read a secret, publish a package or open an admin dashboard.

Kubernetes RBAC only answers that question for Kubernetes API resources. It does not decide whether a user can click a button inside a custom dashboard or whether a service may perform a hardware power action. That application-level permission model must be designed separately.

For this homelab, the first step is identity through Keycloak. More advanced systems such as OpenFGA, SpiceDB or Casbin become interesting only when simple roles and groups are not enough.

---

## Scope

This is broader than Kubernetes RBAC. Kubernetes RBAC controls access to Kubernetes resources. Application authorization controls what users and services can do inside the applications themselves.

Both are needed.

---

## Candidate Systems

| Name | Path | Category | Best fit | Recommendation |
|---|---|---|---|---|
| Keycloak | [docs](./keycloak) · [chart](../../../../helm-charts/infrastructure/platform/security/rights-management/keycloak) · [config](./keycloak/terraform) | Identity provider | OIDC, OAuth2, SSO, realms, clients, users and roles | Best first choice |
| Authentik | [Authentik docs](https://docs.goauthentik.io/docs/) | Identity provider | Modern self-hosted identity with strong UX | Good alternative |
| Zitadel | [Zitadel docs](https://zitadel.com/docs) | Identity provider | Cloud-native identity provider and OIDC/OAuth2 learning | Good alternative |
| OpenFGA | [OpenFGA docs](https://openfga.dev/docs) | Authorization | Relationship-based authorization for app permissions | Later if needed |
| SpiceDB | [SpiceDB docs](https://authzed.com/docs/spicedb) | Authorization | Zanzibar-style permission graph | Advanced/later |
| Casbin | [Casbin docs](https://casbin.org/docs/overview) | Authorization library | Embedded authorization inside application code | Lightweight fallback |

---

## Best First Choice

Use [Keycloak](./keycloak) first.

It is the strongest default for this project because it solves the immediate platform problem: users, login, OIDC/OAuth2, SSO, clients, service accounts and roles. Most dashboards, APIs and developer tools understand OIDC, so Keycloak becomes the central identity provider that other systems can trust.

OpenFGA, SpiceDB and Casbin solve a different problem. They are about fine-grained authorization inside applications. They do not replace an identity provider. Add them later only if simple roles and groups are not enough.

---

## Recommended Direction

Start with identity first, then authorization:

1. Use Keycloak first for login, OIDC, OAuth2, SSO and service identities.
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
../../../../helm-charts/infrastructure/platform/security/rights-management/
```

---

## References

- [Keycloak documentation](https://www.keycloak.org/documentation)
- [Authentik documentation](https://docs.goauthentik.io/docs/)
- [Zitadel documentation](https://zitadel.com/docs)
- [OpenFGA documentation](https://openfga.dev/docs)
- [SpiceDB documentation](https://authzed.com/docs/spicedb)
- [Casbin documentation](https://casbin.org/docs/overview)
- [Wikipedia: Authorization](https://en.wikipedia.org/wiki/Authorization)
- [Wikipedia: Role-based access control](https://en.wikipedia.org/wiki/Role-based_access_control)
- [Wikipedia: Access-control list](https://en.wikipedia.org/wiki/Access-control_list)
- [Wikipedia: OAuth](https://en.wikipedia.org/wiki/OAuth)
