# Ingress And External Access

[<- Back to Platform](../README.md)

This directory documents how HTTP(S) traffic reaches applications on the cluster — from inside the LAN and from the internet.

Three concerns live here because they are decided together:

- **Ingress routing**: which request reaches which service ([Traefik](./traefik))
- **TLS**: how HTTPS certificates are created and renewed ([cert-manager](./cert-manager))
- **External access**: how devices outside the LAN reach selected apps without VPN or port forwarding ([Cloudflare Tunnel](./cloudflare-tunnel))
- **Private access**: how admin devices reach everything else, mesh-VPN style ([NetBird](./netbird))

An ingress controller is a Kubernetes-aware reverse proxy. A browser sends a request to a hostname such as `grafana.home.example.com`. The ingress controller receives that request, checks the configured routing rules and forwards it to the right Kubernetes Service.

Without an ingress controller, each web application would need to be exposed separately through a NodePort, LoadBalancer IP or manual reverse proxy rule. That becomes messy quickly. Ingress centralizes HTTP and HTTPS entrypoints.

The ingress controller is not the same as [MetalLB](../../kubernetes/metallb). MetalLB gives the ingress controller a reachable IP address. The ingress controller decides which HTTP request goes to which service. And [DNS](../dns) is what makes the hostnames resolve to that IP in the first place.

---

## Why This Matters

Most human-facing applications are reached through HTTP or HTTPS. Dashboards, APIs, MinIO consoles, Nextcloud and many developer tools need stable URLs. Ingress makes those URLs manageable.

Ingress also creates a natural place for TLS termination, redirects, middleware, authentication integration and request routing. In a homelab, this is where internal DNS names become useful. In companies, ingress is a major security and reliability boundary.

External access is documented in the same place because it is the same decision seen from outside: which services get a URL, and who may reach it. The tunnel deliberately publishes individual apps — it is not a VPN and grants no network access.

---

## Components

| Name | Path | Status | Recommendation | Role |
|---|---|---|---|---|
| Traefik | [docs](./traefik) · [chart](../../../helm-charts/infrastructure/platform/ingress/traefik) · [config](./traefik/terraform) | ⚫ Inactive | Homelab standard | Ingress controller and reverse proxy |
| cert-manager | [docs](./cert-manager) · [chart](../../../helm-charts/infrastructure/platform/ingress/cert-manager) · [config](./cert-manager/terraform) | ⚫ Inactive | Strongly recommended | Automatic TLS certificate management |
| Cloudflare Tunnel | [docs](./cloudflare-tunnel) · [chart](../../../helm-charts/infrastructure/platform/ingress/cloudflare-tunnel) · [config](./cloudflare-tunnel/terraform) | ⚫ Inactive | Recommended for remote app access | Publish selected apps externally without port forwarding |
| NetBird | [docs](./netbird) · [chart](../../../helm-charts/infrastructure/platform/ingress/netbird) · [config](./netbird/terraform) | ⚫ Inactive | Candidate for private/admin access | WireGuard mesh with built-in reverse proxy — may replace Cloudflare Tunnel |
| Caddy | [docs](./caddy) | ⚫ Inactive | Documented alternative to Traefik | Reverse proxy with automatic HTTPS; best outside Kubernetes |

---

## Recommended Choice

Start with [Traefik](./traefik) or ingress-nginx. Both are valid.

For this homelab, [Traefik](./traefik) is the first candidate because it is easy to operate, has a useful dashboard and fits smaller clusters well. ingress-nginx is the more conservative default when compatibility with common examples matters most.

| Alternative | Notes |
|---|---|
| Traefik | Good UX, simple operations, strong homelab fit |
| ingress-nginx | Very common, huge ecosystem, predictable behavior |
| [Caddy](./caddy) | Simplest automatic-HTTPS proxy; shines outside Kubernetes |
| HAProxy Ingress | Powerful, less beginner-friendly |
| Gateway API controllers | Future-facing, worth evaluating later |

Do not run multiple ingress controllers unless there is a clear reason and ingress class separation.

---

## Traffic Paths

```text
LAN device                     Internet device
    │                                │
    │ DNS: AdGuard/CoreDNS           │ DNS: Cloudflare
    ▼                                ▼
MetalLB IP ──► Traefik ◄── cloudflared tunnel (outbound-only)
                  │
        TLS via cert-manager
                  │
                  ▼
          Kubernetes Service
```

Both paths converge on the same ingress controller, so routing rules, TLS and middleware are defined once.

---

## Deployment Rule

Deployment assets follow the repository convention:

```text
../../../helm-charts/infrastructure/platform/ingress/<component>/    # Helm chart, mirrors this tree
./<component>/terraform/                           # optional Terraform (e.g. Cloudflare zone/tunnel config)
```

---

## Learning Links

- [Kubernetes Ingress documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Wikipedia: Reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy)
- [Wikipedia: HTTP](https://en.wikipedia.org/wiki/HTTP)
- [Wikipedia: Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security)
