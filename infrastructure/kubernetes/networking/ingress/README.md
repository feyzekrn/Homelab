# Ingress Controller

[<- Back to Kubernetes Networking](../README.md)

An ingress controller is the HTTP and HTTPS entrypoint for applications running in the cluster.

It watches Kubernetes `Ingress` resources and routes incoming traffic to the correct service.

---

## Recommended Choice

Start with [Traefik](../traefik) or ingress-nginx. Both are valid.

For this homelab, [Traefik](../traefik) is the recommended first candidate because it is easy to operate, has a useful dashboard and fits smaller clusters well. ingress-nginx is the more conservative default when compatibility with common examples matters most.

---

## Used For

- HTTP routing
- HTTPS termination
- routing dashboards and APIs
- internal service URLs
- testing production-like web exposure

---

## Alternatives

| Alternative | Notes |
|---|---|
| Traefik | Good UX, simple operations, strong homelab fit |
| ingress-nginx | Very common, huge ecosystem, predictable behavior |
| HAProxy Ingress | Powerful, less beginner-friendly |
| Gateway API controllers | Future-facing, worth evaluating later |

---

## Runtime Status

The ingress controller is currently `⚫ Inactive`. One ingress controller should run permanently once services are exposed through HTTP(S). Do not run multiple ingress controllers unless there is a clear reason and class separation.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/networking/ingress/
```
