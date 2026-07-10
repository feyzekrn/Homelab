# Caddy

[<- Back to Ingress](../README.md)

Caddy is an open-source web server and reverse proxy written in Go, famous for one feature above all: **automatic HTTPS by default**. Point it at a domain and it obtains, renews and serves Let's Encrypt certificates without any configuration.

In this homelab, Caddy is documented as the **main alternative** to [Traefik](../traefik). This project runs Kubernetes, and there Traefik's ingress integration, CRD middleware and ecosystem win. But for the very common homelab setup this repository's readers may start from — a single host with docker-compose — Caddy is arguably the better first reverse proxy, and any honest ingress comparison has to include it.

The core idea: a `Caddyfile` with three lines replaces what takes dozens of lines in nginx, including TLS:

```text
cloud.example.com {
    reverse_proxy nextcloud:80
}
```

That is a complete, production-grade HTTPS reverse proxy definition. Certificates, renewals, HTTP-to-HTTPS redirects, OCSP stapling and modern TLS defaults are all automatic.

---

## Why It Is Documented

Caddy earns a page even though it is not the chosen tool:

- it is the simplest possible entry into reverse proxies and TLS — ideal for the pre-Kubernetes phase of a homelab
- automatic HTTPS made an entire class of configuration errors disappear; understanding *why* teaches good TLS habits
- comparing it against Traefik shows what Kubernetes-native actually means: watching cluster resources vs. editing a config file
- it remains useful *around* the cluster: a Caddy on a small VPS is a clean TLS entry point, e.g. in front of a self-hosted [NetBird](../netbird) deployment or any service that lives outside Kubernetes

The reason it is not chosen here: Caddy's Kubernetes ingress controller is far less mature than Traefik or ingress-nginx. Inside the cluster, ingress rules should come from Kubernetes resources via GitOps, not from a hand-maintained Caddyfile.

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

- Kubernetes ingress controller exists but is immature compared to Traefik/ingress-nginx.
- Config-file mindset fits GitOps-managed clusters poorly.
- Plugins require rebuilding the binary with `xcaddy` (no dynamic loading).
- Smaller middleware ecosystem than Traefik's CRD-based one.
- In this repository's architecture there is simply no gap for it to fill inside the cluster.

---

## Infrastructure Dependencies

If a reader deploys it (outside Kubernetes, its natural habitat):

| Dependency | Purpose |
|---|---|
| A public DNS name | Required for automatic Let's Encrypt certificates |
| [`../../dns/duckdns`](../../dns/duckdns) | Free hostname option for readers without a domain |
| Port 80/443 reachability | HTTP-01/TLS-ALPN-01 challenges need inbound access |

---

## Comparison Notes

| System | Best at | Tradeoff |
|---|---|---|
| Caddy | Zero-config HTTPS, simplest possible setup | Weak Kubernetes-native story |
| [Traefik](../traefik) | Kubernetes-native ingress, CRD middleware (chosen here) | More concepts to learn upfront |
| ingress-nginx | Predictable Kubernetes standard | Manual TLS wiring via cert-manager |
| nginx (plain) | Ubiquitous, infinitely documented | Verbose config, manual certificates |

The short version: on a docker host, start with Caddy. On Kubernetes, use Traefik with [cert-manager](../cert-manager) — which together provide exactly the automatic-HTTPS experience Caddy pioneered, but driven by cluster resources.

---

## Runtime Status

Caddy is `⚫ Inactive` and not planned for the cluster. [Traefik](../traefik) is the chosen ingress controller; this page exists for comparison and as the recommended entry point for readers who are not on Kubernetes yet.

---

## Future Deployment Link

If it were deployed (e.g. as a VPS entry point), configuration would follow the component convention:

```text
../../../../helm-charts/infrastructure/platform/ingress/caddy/
```

---

## Documentation

- [Caddy documentation](https://caddyserver.com/docs/)
- [Caddyfile tutorial](https://caddyserver.com/docs/caddyfile-tutorial)
- [Caddy GitHub](https://github.com/caddyserver/caddy)
- [Wikipedia: Caddy (web server)](https://en.wikipedia.org/wiki/Caddy_(web_server))
