# Traefik

[<- Back to Kubernetes Networking](../README.md)

Traefik is the preferred first ingress controller for this homelab.

It acts as a Kubernetes-aware reverse proxy. It watches Kubernetes resources, receives HTTP and HTTPS traffic and routes requests to the correct service.

---

## Why It Fits

Traefik is a good homelab standard because it is easy to install, has strong Kubernetes integration and is comfortable for smaller clusters. It also gives a useful dashboard for understanding routing behavior.

For a business standard, ingress-nginx, Traefik Enterprise or cloud/provider-specific ingress controllers may be evaluated depending on operational requirements.

---

## Used For

- HTTP and HTTPS routing
- dashboard exposure
- API exposure
- internal service URLs
- TLS termination with cert-manager
- reverse proxy learning

---

## Application Examples

- `grafana.homelab.local` routes to Grafana.
- `api.homelab.local` routes to a backend API service.
- `minio.homelab.local` routes to the MinIO console.
- `dapr-dashboard.homelab.local` routes to a runtime dashboard if enabled.

---

## Comparison Notes

| System | Location | Homelab fit | Business fit | Notes |
|---|---|---|---|---|
| Traefik | Self-hosted | Recommended | Good, depending on requirements | Good UX and simple operations |
| ingress-nginx | Self-hosted | Good | Very common standard | Huge ecosystem and predictable behavior |
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

Traefik is currently `⚫ Inactive`. It should become the first ingress controller once services need HTTP(S) access.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/networking/traefik/
```

---

## Documentation

- [Traefik Kubernetes documentation](https://doc.traefik.io/traefik/setup/kubernetes/)
- [Traefik Helm chart](https://github.com/traefik/traefik-helm-chart)
