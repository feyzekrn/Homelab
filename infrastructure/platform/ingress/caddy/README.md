# Caddy

[<- Back to Ingress](../README.md)

Caddy is an open-source web server and reverse proxy written in Go, famous for one feature above all: **automatic HTTPS by default**. Point it at a domain and it obtains, renews and serves Let's Encrypt certificates without any configuration.

In this homelab, Caddy is the **chosen reverse proxy for the Proxmox world**: it serves the family applications running as containers on [`pve0`](../../../../setup/compute/proxmox-cluster), while [Traefik](../traefik) serves the Kubernetes cluster. Two proxies, two failure domains — deliberately.

The core idea: a `Caddyfile` with three lines replaces what takes dozens of lines in nginx, including TLS:

```text
cloud.example.com {
    reverse_proxy nextcloud:80
}
```

That is a complete, production-grade HTTPS reverse proxy definition. Certificates, renewals, HTTP-to-HTTPS redirects, OCSP stapling and modern TLS defaults are all automatic.

---

## Why It Is Chosen For The Proxmox Side

The family applications — Jellyfin, Immich, Nextcloud — run as containers on the Proxmox host, not on the cluster. They need an entrance, and it must not be the cluster's:

- **Failure domains stay separate.** If those apps were routed through Traefik, rebuilding the cluster would take the family's photos and films offline with it. That is exactly the dependency this architecture avoids.
- **There is nothing dynamic to discover.** Traefik's strength is watching Kubernetes resources and reconfiguring itself. On a Proxmox host there are no such resources — a second Traefik would be a Kubernetes-shaped tool used without Kubernetes, configured through files anyway, but with a far more complex syntax.
- **Two lines per application, and TLS is solved.** No cert-manager, no issuers, no annotations — Caddy obtains and renews certificates by itself, which is the right amount of machinery for five static backends.
- **The Caddyfile is versionable.** It is a small, readable file that belongs in Git next to everything else — the same "config as code" goal, without a control plane to run it.

Inside the cluster the calculation reverses, and that is why it stays [Traefik](../traefik) there: ingress rules should come from Kubernetes resources via GitOps, not from a hand-maintained file. Caddy's own Kubernetes ingress controller is also markedly less mature.

---

## Used For

- reverse proxy with zero-config HTTPS on docker-compose or bare hosts
- TLS entry point on a VPS in front of self-hosted services
- static file serving and simple web hosting
- HTTP/3 experiments (enabled by default)
- learning TLS, redirects and reverse proxying with minimal friction

---

## Strengths

- Automatic HTTPS by default — certificates are a non-topic.
- The `Caddyfile` is the most readable proxy config format in existence.
- Single Go binary, no dependencies, runs anywhere.
- HTTP/3 and modern TLS defaults out of the box.
- On-demand TLS: can issue certificates dynamically per hostname.

---

## Weaknesses

- Kubernetes ingress controller exists but is immature compared to Traefik/ingress-nginx — which is why it stays out of the cluster.
- Config-file mindset fits GitOps-managed clusters poorly (outside the cluster it is an advantage).
- Plugins require rebuilding the binary with `xcaddy` (no dynamic loading).
- Smaller middleware ecosystem than Traefik's CRD-based one.
- No dynamic discovery: every new container has to be added to the Caddyfile by hand.

---

## Infrastructure Dependencies

| Dependency | Purpose |
|---|---|
| An own domain | Required for automatic Let's Encrypt certificates |
| DNS-01 challenge via the Cloudflare API | Issues certificates without any inbound port being open |
| [`adguard-home`](../../dns/adguard-home) | Split DNS: resolves the app hostnames to this proxy internally |
| [`cloudflare-tunnel`](../cloudflare-tunnel) | The external path — the tunnel connector delivers requests to Caddy locally |
| [`zfs-nas`](../../storage/zfs-nas) | Not a proxy dependency, but the reason these apps live here: their datasets are bind-mounted locally |

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Caddy | Zero-config HTTPS, simplest possible setup (chosen outside the cluster) | Weak Kubernetes-native story |
| [Traefik](../traefik) | Kubernetes-native ingress, CRD middleware (chosen inside the cluster) | More concepts to learn upfront |
| ingress-nginx | Predictable Kubernetes standard | Manual TLS wiring via cert-manager |
| Nginx Proxy Manager | Click-together UI, popular in homelabs | GUI state instead of a file in Git |
| nginx (plain) | Ubiquitous, infinitely documented | Verbose config, manual certificates |

The short version: on a container host, Caddy. On Kubernetes, Traefik with [cert-manager](../cert-manager) — which together provide exactly the automatic-HTTPS experience Caddy pioneered, but driven by cluster resources.

---

## Runtime Status

`⚫ Inactive` — planned as a container on [`pve0`](../../../../setup/compute/proxmox-cluster), alongside the family applications it will serve. It is one of the first services to deploy there, because it is what makes those apps reachable under real hostnames.

---

## Configuration Link

The Caddyfile and any supporting configuration live next to this page:

```text
infrastructure/platform/ingress/caddy/terraform/
```

---

## Documentation

- [Caddy documentation](https://caddyserver.com/docs/)
- [Caddyfile tutorial](https://caddyserver.com/docs/caddyfile-tutorial)
- [Caddy GitHub](https://github.com/caddyserver/caddy)
- [Wikipedia: Caddy (web server)](https://en.wikipedia.org/wiki/Caddy_(web_server))
