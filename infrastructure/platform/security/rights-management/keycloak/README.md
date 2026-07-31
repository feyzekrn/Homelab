# Keycloak

[<- Back to Rights Management](../README.md)

Keycloak is the **chosen identity provider** for this homelab.

It provides login, single sign-on, OIDC, OAuth2, realms, clients, users, groups, roles and service accounts. In practical terms: Keycloak is the system other apps trust when they need to know who a user or service is.

It is also the one platform component with consumers in **both worlds** — the family apps on [`pve0`](../../../../../setup/compute/proxmox-cluster) and the admin tooling on the cluster — which makes its placement the most consequential in this catalog. That decision has its own section below.

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

## Prerequisites

**Interim phase (LXC on `pve0`, before the cluster exists):**

| Requirement | Why |
|---|---|
| Proxmox VE running | Both Keycloak and its database are containers |
| PostgreSQL LXC | Created in its **final** shape now, so only the app migrates later |
| [Caddy](../../../ingress/caddy) | Keycloak is extremely particular about hostnames and TLS — get this right first |
| An own domain | The issuer URL must be stable; changing it later means reconfiguring every client |
| [Vaultwarden](../../password-manager/bitwarden) | To hold the admin and break-glass credentials |

**Target phase (anchored on the cluster):**

| Requirement | Why |
|---|---|
| [Bootstrap](../../../../kubernetes/bootstrap) with the anchor node joined and labelled | `homelab/world=pve` is what the pin matches on |
| [Cilium](../../../../kubernetes/cilium) + [MetalLB](../../../../kubernetes/metallb) + [Traefik](../../../ingress/traefik) | Reachable under the same hostname as before |
| The PostgreSQL LXC still on `pve0` | Unchanged — moving it into the cluster would undo the anchor |
| [Vault](../../secret-store) + [External Secrets](../../external-secrets) | Client secrets and the database password |

**Decide the hostname before anything else.** Keycloak bakes its issuer URL into every token and every client configuration. Changing it after clients exist means touching all of them, and it is the single most common cause of a painful Keycloak rebuild.

---

## Where It Runs — The Hardest Placement In The Catalog

| | |
|---|---|
| **Runs on** | `k8s` — with one replica **pinned to the Proxmox-hosted node** |
| **Database** | PostgreSQL as an `lxc` on [`pve0`](../../../../../setup/compute/proxmox-cluster) — deliberately *not* on cluster storage |
| **Consumers** | Both worlds: family apps on `pve0`, admin tooling on the cluster |

Every other component in this catalog belongs cleanly to one world. Keycloak does not, and that creates a real conflict with the [availability rule](../../../../../setup/compute/README.md): the family apps live on `pve0` precisely so that cluster experiments cannot reach them — but if their *login* depends on a cluster workload, rebuilding the cluster locks the family out of their own photos. The dependency would come back through the front door.

**The resolution is an anchor, not a move.** A VM on `pve0` permanently joins the cluster as a node, and critical workloads are constrained to always keep one replica there. Keycloak runs with three replicas: two on the Tiny nodes, one on the Proxmox-hosted node. Wipe the three Tinys and a Keycloak instance is still running, on a machine that was never part of the experiment.

### The part that is easy to get wrong

**Keycloak pods are stateless. The database is the actual single point of failure.**

Realms, users, clients and sessions all live in PostgreSQL. If that database runs on [Longhorn](../../../storage/longhorn) replicated across the three Tiny nodes, the pinned replica buys nothing — the cluster goes, the database goes with it, and the surviving pod has nothing to authenticate against. The anchor only works if the database is anchored too, which is why Keycloak's PostgreSQL is an LXC on `pve0` rather than a cluster workload.

Two operational consequences worth knowing before building this:

- **Running pods survive a control-plane outage.** Kubelet does not stop pods when the API server is unreachable, so the pinned replica keeps serving logins while the Tiny nodes are being rebuilt. But if that pod crashes during the window, nothing reschedules it. Closing that gap means making the Proxmox-hosted node a control-plane member — which argues for 2 Tinys + the VM as the control plane rather than 3 Tinys + a worker, to keep the etcd count odd.
- **Pin with a topology constraint, not a second Deployment.** A `topologySpreadConstraint` over a node label (`homelab/world=pve` versus `homelab/world=k8s`) with `whenUnsatisfiable: DoNotSchedule` keeps this as one release object. A separate pinned Deployment with a `nodeSelector` creates two things that drift apart on the next upgrade.

### Why not simply run it on `pve0`

It would work, and it would be simpler. It is rejected for two reasons. Keycloak is the component this project most wants to operate the way it is operated professionally — the Operator, realm CRDs, OIDC clients driven from Git — and that only exists on Kubernetes. And the anchor pattern itself is worth building once: it generalizes to every future workload that serves both worlds, which is the more useful thing to own than one more container on the hypervisor.

The honest counterpoint: if Keycloak runs for a year on `pve0` without incident, moving it into the cluster later buys learning, not availability. The migration is cheap either way — export the realm as JSON, import it, repoint the issuer URL in each client — so starting on `pve0` and moving in is a legitimate path, and the one this project takes while the cluster does not yet exist.

### Interim state

The cluster is not running yet, and the family apps should not wait for it. Keycloak therefore **starts as an LXC on `pve0`** together with its PostgreSQL, and migrates into the cluster once it exists. The database container is created in its final shape from the beginning, so the migration only moves the application, not the state.

---

## Recommended Homelab Model

Start with one realm for the homelab:

```text
Realm: homelab
```

Then add clients gradually:

| Client | Purpose | World |
|---|---|---|
| `nextcloud` | Family login via the `user_oidc` app | `pve0` |
| `immich` | Family login via native OIDC | `pve0` |
| `grafana` | Grafana OIDC login | `k8s` |
| `dashboard-web` | Browser login for the web dashboard | `k8s` |
| `dashboard-api` | Backend API token validation | `k8s` |
| `artifact-repository` | Nexus or Artifactory SSO | `k8s` |
| `node-control-api` | Service identity for hardware-control APIs | `k8s` |

**[Jellyfin](../../../../../applications/jellyfin) is deliberately missing from that list.** It has no first-class OIDC support — only a third-party plugin that tends to break across releases — so the media server keeps local accounts. That is an acceptable exception: Jellyfin holds no personal data beyond watch state, and a broken login plugin on the TV is a support call nobody wants.

Use groups for broad access levels:

| Group | Purpose |
|---|---|
| `homelab-admins` | Full administrative access |
| `homelab-operators` | Operational access without full ownership |
| `homelab-viewers` | Read-only dashboards and status pages |
| `service-accounts` | Machine identities |
| `family` | Household members — Nextcloud and Immich only, no admin surface |

The `family` group is the one that must stay boring. Its members are not operators of this homelab; they are users of it, and every capability they do not need is one that cannot be misused by accident.

---

## Break-Glass Access

One rule that follows directly from making Keycloak the only door: **there has to be a second door, and it has to be documented before it is needed.**

- Each app keeps **one local admin account**, disabled from normal use but not deleted. Disabling local login entirely means a Keycloak outage locks out the person who has to fix Keycloak.
- Those credentials live in [Vaultwarden](../../password-manager/bitwarden) on `pve0` — in the stable world, reachable when the cluster is not.
- The Keycloak admin account itself is **not** an OIDC account and never depends on Keycloak being healthy.

This is the piece most homelab SSO setups skip, and it is the one that turns a two-hour outage into a weekend.

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

Keycloak is currently `⚫ Inactive`. It is the **chosen identity provider** and one of the earlier components to build, because the family apps are meant to launch with SSO rather than be migrated onto it later — retrofitting identity means re-creating every account.

The build order is deliberate:

1. PostgreSQL as an LXC on `pve0` (its final home, created first).
2. Keycloak as an LXC on `pve0`, realm `homelab`, one test client.
3. One clean login flow end to end — Nextcloud first, since its OIDC support is the strongest.
4. The remaining clients, one at a time.
5. Once the cluster runs: migrate the application into `k8s` with the pinned replica, keep the database where it is.

Do not connect every service immediately. One proven login flow is worth more than five half-configured ones.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../../helm-charts/infrastructure/platform/security/rights-management/keycloak/
```

---

## Documentation

- [Keycloak documentation](https://www.keycloak.org/documentation)
- [Keycloak Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/)
- [Keycloak Securing Applications Guide](https://www.keycloak.org/docs/latest/securing_apps/)
- [Keycloak Operator documentation](https://www.keycloak.org/operator/)
- [Wikipedia: Keycloak](https://en.wikipedia.org/wiki/Keycloak)
- [Wikipedia: OpenID Connect](https://en.wikipedia.org/wiki/OpenID_Connect)
- [Wikipedia: OAuth](https://en.wikipedia.org/wiki/OAuth)
- [Wikipedia: Single sign-on](https://en.wikipedia.org/wiki/Single_sign-on)
