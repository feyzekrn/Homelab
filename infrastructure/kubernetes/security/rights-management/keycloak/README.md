# Keycloak

[<- Back to Rights Management](../README.md)

Keycloak is the recommended first identity provider for this homelab.

It provides login, single sign-on, OIDC, OAuth2, realms, clients, users, groups, roles and service accounts. In practical terms: Keycloak is the system other apps trust when they need to know who a user or service is.

---

## Why It Is The Best First Choice

Keycloak solves the identity layer before the project needs complex authorization.

That matters because most services need identity before they need advanced permission graphs:

- dashboards need user login
- APIs need access tokens
- internal services need service accounts
- admin tools need roles
- package registries and secret systems may need SSO

Keycloak is mature, self-hosted, widely supported and speaks the protocols most modern tools expect: OIDC, OAuth2 and SAML.

---

## What Keycloak Is Used For

- user login for dashboards and admin tools
- SSO across homelab web services
- OIDC provider for custom APIs
- OAuth2 clients for frontend and backend apps
- service accounts for machine-to-machine access
- groups and roles for coarse-grained permissions
- identity source for future rights-management decisions

---

## Application Examples

- The admin dashboard redirects users to Keycloak for login.
- A Go API validates JWT access tokens issued by Keycloak.
- Grafana uses Keycloak as an OIDC login provider.
- The Artifact Repository uses Keycloak-backed SSO for developer access.
- A `node-control-api` service account receives a token for internal calls.
- Users in the `homelab-admins` group can access admin-only dashboard routes.

---

## Recommended Homelab Model

Start with one realm for the homelab:

```text
Realm: homelab
```

Then add clients gradually:

| Client | Purpose |
|---|---|
| `dashboard-web` | Browser login for the web dashboard |
| `dashboard-api` | Backend API token validation |
| `grafana` | Grafana OIDC login |
| `artifact-repository` | Nexus or Artifactory SSO |
| `node-control-api` | Service identity for hardware-control APIs |

Use groups for broad access levels:

| Group | Purpose |
|---|---|
| `homelab-admins` | Full administrative access |
| `homelab-operators` | Operational access without full ownership |
| `homelab-viewers` | Read-only dashboards and status pages |
| `service-accounts` | Machine identities |

---

## Keycloak vs Alternatives

| System | Best at | Tradeoff |
|---|---|---|
| Keycloak | Mature self-hosted identity, OIDC/OAuth2, SSO, roles and realms | Heavier than newer homelab-friendly tools |
| Authentik | Great self-hosted UX and modern identity workflows | Smaller ecosystem than Keycloak |
| Zitadel | Modern cloud-native identity platform | Different operating model; may be less familiar |
| OpenFGA | Fine-grained relationship-based authorization | Not an identity provider |
| SpiceDB | Complex permission graphs at scale | Advanced and unnecessary early |
| Casbin | Authorization embedded directly in apps | Less centralized; app code owns more logic |

For this project, Keycloak should come first. OpenFGA or SpiceDB can be added later if app permissions outgrow Keycloak groups and roles.

---

## How It Connects To The Rest

Keycloak should eventually integrate with:

- Traefik or an auth proxy for protected web routes
- Grafana for dashboard login
- Artifact Repository for developer SSO
- Secret Store for admin and operator access
- custom services under `services/`
- Kubernetes RBAC only where cluster access is needed

Keycloak should not store application secrets. It manages identity and tokens. The Secret Store manages sensitive credentials.

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`, but the first evaluation can use the Keycloak Operator or a Helm chart.

For a Kubernetes-native setup, evaluate the official Operator path first:

```text
1. Install the Keycloak Operator.
2. Create a Keycloak instance.
3. Create the `homelab` realm.
4. Create one test OIDC client.
5. Connect one simple app or Grafana to Keycloak.
```

Do not connect every service immediately. First prove one clean login flow end to end.

---

## Runtime Status

Keycloak is currently `⚫ Inactive`. It should become the first Rights Management component once the dashboard, API layer or developer tools need login and SSO.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/security/rights-management/keycloak/
```

---

## Documentation

- [Keycloak documentation](https://www.keycloak.org/documentation)
- [Keycloak Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/)
- [Keycloak Securing Applications Guide](https://www.keycloak.org/docs/latest/securing_apps/)
- [Keycloak Operator documentation](https://www.keycloak.org/operator/)
