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

| Name | Path | Status | Runs on | Idle RAM | Recommendation | Role |
|---|---|---|---|---|---|---|
| Traefik | [docs](./traefik) · [chart](../../../helm-charts/infrastructure/platform/ingress/traefik) · [config](./traefik/terraform) | ⚫ Inactive | k8s | ~100–150 MB | Chosen ingress controller for the cluster | Ingress controller and reverse proxy |
| Caddy | [docs](./caddy) · [config](./caddy/terraform) | ⚫ Inactive | lxc | ~30–50 MB | Chosen reverse proxy for the Proxmox world | Static reverse proxy with automatic HTTPS |
| cert-manager | [docs](./cert-manager) · [chart](../../../helm-charts/infrastructure/platform/ingress/cert-manager) · [config](./cert-manager/terraform) | ⚫ Inactive | k8s | ~50–100 MB | Chosen TLS automation (cluster side) | Automatic TLS certificate management |
| Cloudflare Tunnel | [docs](./cloudflare-tunnel) · [chart](../../../helm-charts/infrastructure/platform/ingress/cloudflare-tunnel) · [config](./cloudflare-tunnel/terraform) | ⚫ Inactive | lxc + k8s | ~20–50 MB | Chosen for public app exposure | Publish selected apps externally without port forwarding |
| NetBird | [docs](./netbird) · [config](./netbird/terraform) | ⚫ Inactive | lxc | ~50 MB peer | Chosen for private/admin access | WireGuard mesh, managed control plane |

**Two proxies, two worlds — and that is the point.** Traefik serves the cluster, where it watches Kubernetes resources and configures itself. Caddy serves the Proxmox containers, where there is nothing to watch and a two-line config file per app is the honest answer. Running a second Traefik there would mean using a Kubernetes-shaped tool without Kubernetes.

The reason for the split is a failure domain, not a preference: if the family apps were routed through the cluster's ingress, then rebuilding the cluster would take the photos and films offline with it. Each world keeps its own entrance, so either can be torn down without affecting the other.

Certificates follow the same split: cert-manager issues for the cluster, Caddy obtains its own automatically. [AdGuard Home](../dns/adguard-home) points each hostname at the right entrance internally through split DNS.

---

## Recommended Choice

For the cluster, Traefik is chosen: easy to operate, a useful dashboard, CRD-based middleware and a good fit for small clusters. ingress-nginx would be the more conservative default when compatibility with copy-paste examples matters most.

| Alternative | Notes |
|---|---|
| Traefik | Good UX, simple operations, strong homelab fit — chosen for the cluster |
| Caddy | Simplest automatic-HTTPS proxy; shines outside Kubernetes — chosen for the Proxmox side |
| ingress-nginx | Very common, huge ecosystem, predictable behaviour |
| HAProxy Ingress | Powerful, less beginner-friendly |
| Gateway API controllers | Future-facing, worth evaluating later |

Do not run multiple ingress controllers **inside the cluster** unless there is a clear reason and ingress class separation. Traefik and Caddy are not a violation of that rule: they live in different failure domains and never route the same hostname.

---

## Traffic Paths

```text
                LAN device                          Internet device
                     │                                     │
        DNS: AdGuard (split DNS)                    DNS: Cloudflare
                     │                                     │
        ┌────────────┴────────────┐                        │
        ▼                         ▼                        ▼
   MetalLB IP                 Caddy (LXC)          Cloudflare edge
        │                         │                        │
     Traefik                      │              ┌─────────┴─────────┐
        │                         │              ▼                   ▼
  TLS: cert-manager      TLS: automatic     cloudflared (k8s)  cloudflared (lxc)
        │                         │              │                   │
        ▼                         ▼              ▼                   ▼
 Kubernetes Service      Proxmox container    Traefik              Caddy
```

Internally, split DNS sends each hostname straight to its own entrance — no detour through the internet. Externally, Cloudflare routes each hostname into the connector of the world that owns the app. Both worlds keep their own TLS story, and neither depends on the other being up.

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
