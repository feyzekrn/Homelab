# Ingress Controller

[<- Back to Kubernetes Networking](../README.md)

An ingress controller is the HTTP and HTTPS entrypoint for applications running in the cluster.

It watches Kubernetes `Ingress` resources and routes incoming traffic to the correct service.

An ingress controller is a Kubernetes-aware reverse proxy. A browser sends a request to a hostname such as `grafana.homelab.local`. The ingress controller receives that request, checks the configured routing rules and forwards the request to the right Kubernetes Service.

Without an ingress controller, each web application would need to be exposed separately through a NodePort, LoadBalancer IP or manual reverse proxy rule. That becomes messy quickly. Ingress centralizes HTTP and HTTPS entrypoints.

The ingress controller is not the same as MetalLB. MetalLB gives the ingress controller a reachable IP address. The ingress controller decides which HTTP request goes to which service.

---

## Why This Matters

Most human-facing applications are reached through HTTP or HTTPS. Dashboards, APIs, MinIO consoles, Nextcloud and many developer tools need stable URLs. Ingress makes those URLs manageable.

Ingress also creates a natural place for TLS termination, redirects, middleware, authentication integration and request routing. In a homelab, this is where internal DNS names become useful. In companies, ingress is a major security and reliability boundary.

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
- connecting cert-manager certificates to web services

---

## Strengths

- Gives many applications one shared HTTP(S) entrypoint.
- Keeps URLs stable even if pods move inside the cluster.
- Works naturally with DNS and TLS automation.
- Reduces the need to expose every application directly.
- Teaches a core production Kubernetes pattern.

---

## Weaknesses

- Only solves HTTP and HTTPS by default; arbitrary TCP/UDP needs separate handling.
- Misconfigured routing rules can expose the wrong service.
- Authentication is not automatic; it must be added through apps, middleware or an auth proxy.
- Running multiple ingress controllers requires clear ingress class separation.

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

---

## Learning Links

- [Kubernetes Ingress documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Wikipedia: Reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy)
- [Wikipedia: HTTP](https://en.wikipedia.org/wiki/HTTP)
- [Wikipedia: Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security)
