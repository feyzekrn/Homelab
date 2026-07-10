# NetBird

[<- Back to Ingress](../README.md)

NetBird is an open-source, WireGuard-based overlay network: all devices join a private mesh with a central management plane, SSO login, access policies and routing — self-hostable or as a managed cloud.

In this homelab, NetBird is the **chosen private access path**: the "VPN side" of the trust rule documented in [Cloudflare Tunnel](../cloudflare-tunnel#trust-decision). Admin interfaces (Kubernetes API, SSH, MikroTik, Grafana) stay off any public tunnel — NetBird is how personal devices reach them securely from anywhere.

What makes NetBird more than a VPN is its **built-in reverse proxy** (since v0.65): selected internal services can be exposed to the public internet with automatic Let's Encrypt TLS, custom domains and optional authentication (SSO/OIDC, password or PIN) — traffic enters at a NetBird ingress point and travels through the encrypted mesh to the target, with no open ports on the homelab. That is exactly the job [Cloudflare Tunnel](../cloudflare-tunnel) does here. The decision for this homelab: **NetBird handles private/admin access, Cloudflare Tunnel handles public app exposure** — with the reverse proxy documented as the consolidation option if one system should ever do both.

---

## Why It Fits

NetBird matches this repository's philosophy unusually well:

- fully open source (BSD-3), self-hostable management plane — no dependency on a closed control plane
- native OIDC support: [Keycloak](../../security/rights-management/keycloak) becomes the identity provider for network access, the same accounts as everywhere else
- WireGuard underneath: modern, fast, auditable crypto
- access policies and groups: the family's devices see Nextcloud, admin devices see everything
- routing peers: one agent in the cluster can expose internal services to the mesh without installing anything else
- the reverse proxy feature covers the public-exposure use case on top

It is also a realistic platform test: running the management plane, relay and signal services self-hosted is a real multi-service deployment with real availability questions.

---

## The Reverse Proxy Feature (vs. Cloudflare Tunnel)

The overlap deserves its own decision note:

| Aspect | NetBird Reverse Proxy | Cloudflare Tunnel |
|---|---|---|
| Public entry point | NetBird Cloud ingress, or self-hosted (must be publicly reachable) | Cloudflare's global edge |
| TLS | Let's Encrypt automatic, custom domains | Cloudflare edge certificates |
| Auth in front of apps | SSO (OIDC), password or PIN built in | Cloudflare Access |
| Traffic path | Encrypted WireGuard mesh end to end | Terminated and proxied at Cloudflare |
| Open source | Yes, including server | Connector only; edge is proprietary |
| Self-hosted requirement | Traefik with TLS passthrough as external proxy; L4 services need dedicated ports | Only outbound `cloudflared` |
| DDoS protection | None built in (self-hosted) | Included |

The honest summary: **with NetBird Cloud, Cloudflare Tunnel becomes largely redundant** — one system handles VPN and public exposure with better privacy (no third party terminating TLS mid-path in the same way). **Fully self-hosted**, the public entry point must itself be reachable from the internet (typically a small VPS running the NetBird server), so "no port forwarding at home" still holds, but the edge, availability and DDoS story become your responsibility. This repository uses both — NetBird for private access, Cloudflare Tunnel for public exposure — and revisits consolidation once both run in practice.

---

## Used For

- admin access to Kubernetes API, SSH and network gear from anywhere
- family devices reaching internal services without public exposure
- site-to-site style routing into the cluster via a routing peer
- optionally: public exposure of selected apps via the reverse proxy
- exit node: routing a device's traffic through home when abroad

---

## Strengths

- Open source end to end, self-hostable — fits the homelab philosophy.
- Keycloak/OIDC integration for network identity.
- WireGuard performance with central policy management.
- Reverse proxy can replace a separate tunnel product.
- Cross-platform clients (iOS, Android, macOS, Windows, Linux, Docker).

---

## Weaknesses

- Self-hosting the full stack (management, signal, relay, proxy) is more moving parts than one `cloudflared` container.
- Self-hosted reverse proxy requires Traefik TLS passthrough and public reachability — the hard part Cloudflare otherwise does for you.
- Younger project than WireGuard/Tailscale ecosystems; features move fast.
- Clients must be installed on every participating device (inherent to any VPN).

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| [`../../security/rights-management/keycloak`](../../security/rights-management/keycloak) | OIDC identity provider for peer login |
| [`../traefik`](../traefik) | TLS-passthrough entry for the self-hosted reverse proxy |
| [`../cloudflare-tunnel`](../cloudflare-tunnel) | The overlapping alternative for public exposure |
| [`../../../kubernetes/metallb`](../../../kubernetes/metallb) | Stable IP if the management plane runs on the cluster |
| [`../../storage/longhorn`](../../storage/longhorn) | Persistence for the management database |

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| NetBird | Open-source mesh + built-in public exposure | Self-hosting the full stack is real work |
| Tailscale | Most polished mesh VPN experience | Closed control plane, self-hosted Headscale is unofficial |
| Plain WireGuard | Minimal, no extra services | Manual key/peer management, no SSO |
| [Cloudflare Tunnel](../cloudflare-tunnel) | Zero-effort public exposure with global edge | Third party in the traffic path, not a VPN |

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`.

First evaluation checklist:

1. Start with NetBird Cloud (free tier) to learn the model before self-hosting.
2. Connect Keycloak as the OIDC provider.
3. Enroll one admin laptop and one routing peer inside the cluster network.
4. Define access groups: `admins` see everything, `family` sees app services only.
5. Test reaching the Kubernetes API over the mesh, then close any other admin path.
6. Evaluate the reverse proxy against Cloudflare Tunnel for one public app.
7. Revisit the split (NetBird private + Cloudflare public) once both run — consolidation onto NetBird's reverse proxy stays an option.

---

## Runtime Status

NetBird is currently `⚫ Inactive`. It is the chosen private/admin access path and becomes active as the first piece of the remote-access build.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/ingress/netbird/
```

---

## Documentation

- [NetBird documentation](https://docs.netbird.io/)
- [NetBird Reverse Proxy docs](https://docs.netbird.io/manage/reverse-proxy)
- [NetBird v0.65: Built-in Reverse Proxy](https://netbird.io/knowledge-hub/reverse-proxy)
- [Self-hosted: external reverse proxy setup](https://docs.netbird.io/selfhosted/external-reverse-proxy)
- [NetBird GitHub](https://github.com/netbirdio/netbird)
- [Wikipedia: WireGuard](https://en.wikipedia.org/wiki/WireGuard)
