# Cloudflare Tunnel

[<- Back to Ingress](../README.md)

Cloudflare Tunnel exposes selected homelab services to the internet without opening router ports and without requiring a VPN connection on every device.

A small connector (`cloudflared`) opens an **outbound** connection to Cloudflare's edge. Public requests to configured hostnames (for example `photos.example.com`) arrive at Cloudflare and are relayed through that tunnel to the internal service. The home IP address is never exposed, no inbound firewall rule exists and it works behind CGNAT and changing ISP addresses.

**One connector per world** (`lxc + k8s`). A connector can only reach what it can reach, so each world runs its own: the `lxc` connector on [`pve0`](../../../../setup/compute/proxmox-cluster) delivers to [Caddy](../caddy) for the family apps, and the `k8s` connector delivers to [Traefik](../traefik) for cluster services. Cloudflare routes each hostname into the connector belonging to the world that owns the app. Neither world depends on the other being up — which is the whole reason the split exists.

In this homelab, the tunnel solves one specific everyday problem: personal devices (phones, laptops) should reach services like Nextcloud or Immich from anywhere — mobile network, office, holiday — without first connecting a VPN or maintaining port forwards. Calendar sync, photo upload and file access should just work.

**This is explicitly not a VPN replacement.** A VPN grants network-level access to the LAN; the tunnel publishes individual HTTP(S) services. Administrative access (SSH, Kubernetes API, router UI) stays off the tunnel and behind a VPN or LAN-only access.

---

## Why It Fits

Cloudflare Tunnel fits this homelab because remote access is what makes the "replace iCloud/OneDrive" goal realistic:

- sync clients (Nextcloud, Immich) need the server reachable from everywhere, all the time
- no port forwarding means no exposed home IP and no attack surface on the router
- works regardless of dynamic IPs or CGNAT
- Cloudflare Access can add an authentication layer in front of sensitive apps
- TLS is handled at the Cloudflare edge

It also teaches a modern pattern: outbound-only connectivity for inbound traffic, the same idea behind many zero-trust products.

---

## Prerequisites

| Requirement | Why |
|---|---|
| **An own domain on Cloudflare** | The tunnel routes by hostname; the zone has to be Cloudflare-managed |
| A Cloudflare account + tunnel token | One token per connector, stored in [Vault](../../security/secret-store) |
| A reverse proxy behind it | [Caddy](../caddy) in the `lxc` world, [Traefik](../traefik) in the `k8s` world |
| The target app already working **on the LAN** | The tunnel publishes a service; it does not fix a broken one |
| [Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/policies/access/) | Required in front of anything sensitive — see [Home Assistant](../../../../applications/home-assistant/README.md#access-from-outside) |

**Deploy this last.** Every hostname published here is reachable by the entire internet, so it should only be pointed at a service that already works, already has authentication and is already understood. Publishing first and securing afterwards is how homelabs end up in someone's scan results.

---

## Used For

- reaching Nextcloud sync (files, calendar, contacts) from outside the LAN
- Immich mobile photo backup while away from home
- sharing a link to a self-hosted service with family
- publishing selected read-only dashboards
- avoiding port forwards, dynamic DNS and exposed home IPs

---

## Strengths

- No inbound ports; home IP stays hidden.
- Works behind CGNAT and with changing IPs.
- Free tier covers typical homelab use.
- Optional Cloudflare Access for identity-based gating.
- DDoS protection and edge TLS included.

---

## Weaknesses

- Traffic flows through a third party — Cloudflare terminates TLS and can technically see it.
- Dependency on an external commercial service and its terms.
- Requires a domain managed in Cloudflare DNS.
- Free plan limits: HTTP-focused; large media streaming may violate ToS expectations.
- Not suitable for non-HTTP admin protocols; that remains VPN territory.

---

## Trust Decision

Publishing a service through the tunnel means trusting Cloudflare with that traffic. For this homelab the rule is:

- **Tunnel**: user-facing apps where convenience matters (Nextcloud, Immich, Jellyfin remote access if acceptable).
- **VPN/LAN only**: everything administrative — Kubernetes API, SSH, MikroTik, Grafana admin, secret stores.
- End-to-end sensitive data that must never touch a third party stays LAN/VPN-only too.

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| Cloudflare account + domain | DNS zone and tunnel management |
| [`traefik`](../traefik) | Tunnel targets the ingress, one entrypoint for all apps |
| [`cert-manager`](../cert-manager) | Internal TLS between ingress and apps |
| [`secret-store`](../../security/secret-store) | Tunnel credentials must not live in Git |
| [`keycloak`](../../security/rights-management/keycloak) | App-level login behind the tunnel |

---

## Application Examples

- `cloud.example.com` reaches Nextcloud from any network, so CalDAV/CardDAV sync never breaks.
- `photos.example.com` lets Immich upload holiday photos from mobile data.
- Cloudflare Access in front of a status dashboard, allowing only family Google/GitHub logins.
- Grandparents open a shared Immich album link without any VPN app.

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Cloudflare Tunnel | Zero-port public access to HTTP apps | Third party in the traffic path |
| WireGuard VPN | Full private network access | Client setup on every device, always-on toggling |
| [NetBird](../netbird) | Open-source mesh VPN with built-in reverse proxy | Self-hosting the public entry point is your job |
| Tailscale | Mesh VPN with minimal setup | Also third-party coordinated; per-device install |
| Port forwarding + DynDNS | No middleman | Exposes home IP and router attack surface |
| ngrok | Quick temporary tunnels | Not meant for permanent self-hosting |

This homelab combines two of these: **Cloudflare Tunnel for public app exposure and [NetBird](../netbird) for administrative access**. NetBird's built-in reverse proxy covers the public-exposure job too, so consolidating everything onto NetBird remains a documented option — the comparison lives in the [NetBird docs page](../netbird/README.md#the-reverse-proxy-feature-vs-cloudflare-tunnel).

---

## Hands-On Start

The `k8s` connector is deployed by Helm chart; the `lxc` connector is a Proxmox guest and has no chart.

First evaluation checklist:

1. Move a domain's DNS to Cloudflare (free plan).
2. Create a tunnel and store the credentials in the secret workflow, never in Git.
3. Deploy the **`lxc` connector first**, pointing at [Caddy](../caddy) — the Proxmox world exists before the cluster does, and the family apps are the reason remote access is wanted at all.
4. Publish one harmless test service and verify access from a mobile network.
5. Add Cloudflare Access rules **before** publishing anything personal.
6. Add the `k8s` connector pointing at [Traefik](../traefik) once the cluster serves something worth reaching.
7. Document which services are tunnel-exposed and which are VPN-only.

---

## Runtime Status

Cloudflare Tunnel is currently `⚫ Inactive`. The `lxc` connector becomes relevant as soon as Nextcloud or Immich should sync from outside the LAN — which makes it part of the first Proxmox build rather than a cluster-era component. The `k8s` connector follows later and is genuinely optional: most cluster services are administrative, and administrative access belongs on [NetBird](../netbird), not on a public hostname.

**One caveat worth knowing before relying on it for media:** Cloudflare's terms restrict serving large volumes of video through the proxy. [Jellyfin](../../../../applications/jellyfin) remote streaming is the case that runs into this — NetBird is the safer path for that particular app.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/ingress/cloudflare-tunnel/
```

---

## Documentation

- [Cloudflare Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [cloudflared GitHub](https://github.com/cloudflare/cloudflared)
- [Cloudflare Access documentation](https://developers.cloudflare.com/cloudflare-one/policies/access/)
- [Wikipedia: Cloudflare](https://en.wikipedia.org/wiki/Cloudflare)
- [Wikipedia: Zero trust security model](https://en.wikipedia.org/wiki/Zero_trust_security_model)
