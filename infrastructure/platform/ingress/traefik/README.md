# Traefik

[<- Back to Ingress](../README.md)

Traefik is the **chosen ingress controller for the Kubernetes cluster** (`k8s`).

It acts as a Kubernetes-aware reverse proxy. It watches Kubernetes resources, receives HTTP and HTTPS traffic and routes requests to the correct service.

**It serves the cluster only.** The applications on [`pve0`](../../../../setup/compute/proxmox-cluster) have their own entrance in [Caddy](../caddy), deliberately — routing the family apps through the cluster's ingress would mean a cluster rebuild takes the photos offline with it. Two proxies, two failure domains; they never route the same hostname.

Traefik sits at the edge of the cluster for web traffic. When a request arrives for `grafana.homelab.local`, Traefik looks at Kubernetes routing resources and forwards the request to the Grafana Service. When a request arrives for `api.homelab.local`, it can route to a different backend.

This makes Traefik the front door for many web applications. It does not replace the application itself, and it does not replace the pod network. It is the HTTP reverse proxy that connects hostnames, TLS certificates and Kubernetes Services.

---

## Why It Fits

Traefik is a good homelab standard because it is easy to install, has strong Kubernetes integration and is comfortable for smaller clusters. It also gives a useful dashboard for understanding routing behavior.

For a business standard, ingress-nginx, Traefik Enterprise or cloud/provider-specific ingress controllers may be evaluated depending on operational requirements.

Traefik is also beginner-friendly because its dashboard helps reveal what routing rules exist and whether services are reachable. That makes it easier to learn ingress than a completely invisible proxy setup.

---

## Prerequisites

| Requirement | Why |
|---|---|
| A running cluster with [Cilium](../../../kubernetes/cilium) | Traefik is a pod like any other; the CNI has to work first |
| [MetalLB](../../../kubernetes/metallb) | Traefik needs a routable LoadBalancer IP on the LAN — this is the one that surprises people |
| [cert-manager](../cert-manager) | For HTTPS. Traefik terminates TLS but does not obtain certificates itself |
| An own domain + [AdGuard Home](../../dns/adguard-home) | Split DNS has to point the hostnames at the MetalLB IP internally |
| [Cloudflare Tunnel](../cloudflare-tunnel) | Only for services that should also be reachable from outside |

The MetalLB dependency is the one worth internalising: **an ingress controller with no external IP routes nothing.** [MetalLB](../../../kubernetes/metallb) assigns the address, DNS makes the name resolve to it, and Traefik decides what happens to the request once it arrives. Three different components, three different jobs, and all three have to be right before a single URL works.

---

## Used For

- HTTP and HTTPS routing
- dashboard exposure
- API exposure
- internal service URLs
- TLS termination with cert-manager
- reverse proxy learning
- middleware experiments such as redirects or auth forwarding

---

## Strengths

- Strong Kubernetes integration and automatic discovery.
- Good homelab user experience and useful dashboard.
- Supports Kubernetes Ingress, Traefik CRDs and newer Gateway API paths.
- Works well with cert-manager for HTTPS.
- Simpler first experience than many larger ingress stacks.

---

## Weaknesses

- ingress-nginx has broader example coverage in many Kubernetes tutorials.
- Traefik-specific CRDs can reduce portability if overused.
- The dashboard must be protected before exposing it beyond trusted networks.
- Complex enterprise edge requirements may need a different product or architecture.

---

## Application Examples

- `grafana.homelab.local` routes to Grafana.
- `api.homelab.local` routes to a backend API service.
- `minio.homelab.local` routes to the MinIO console.
- `dapr-dashboard.homelab.local` routes to a runtime dashboard if enabled.
- `nextcloud.homelab.local` uses cert-manager-managed TLS.

---

## Comparison Notes

| System | Location | Homelab fit | Business fit | Notes |
|---|---|---|---|---|
| Traefik | Self-hosted | Recommended | Good, depending on requirements | Good UX and simple operations |
| ingress-nginx | Self-hosted | Good | Very common standard | Huge ecosystem and predictable behavior |
| [Caddy](../caddy) | Self-hosted | Great outside Kubernetes | Niche for k8s ingress | Automatic HTTPS pioneer, weak ingress-controller story |
| HAProxy Ingress | Self-hosted | Advanced | Good | Powerful, less beginner-friendly |
| Gateway API controllers | Self-hosted | Research | Growing standard | Worth revisiting later |

---

## Hands-On Start

Deployment files should eventually live under `helm-charts`, but the basic upstream Helm flow is:

```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik --namespace traefik --create-namespace
```

After installing, expose Traefik through MetalLB and create a test `Ingress` or `IngressRoute`.

---

## Runtime Status

Traefik is currently `⚫ Inactive`. It becomes active once the first cluster service needs a URL — in the build order that is after [Cilium](../../../kubernetes/cilium), [MetalLB](../../../kubernetes/metallb) and [Longhorn](../../storage/longhorn), and together with [cert-manager](../cert-manager).

One operational note before it is exposed: **the dashboard must be protected first.** It reveals the full routing table of the cluster and is reachable by default. It belongs behind [NetBird](../netbird) or an authentication middleware, never on a public hostname.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/infrastructure/platform/ingress/traefik/
```

---

## Documentation

- [Traefik Kubernetes documentation](https://doc.traefik.io/traefik/setup/kubernetes/)
- [Traefik Helm chart](https://github.com/traefik/traefik-helm-chart)
- [Wikipedia: Reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy)
