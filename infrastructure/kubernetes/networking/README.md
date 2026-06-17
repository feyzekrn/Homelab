# Kubernetes Networking

[<- Back to Kubernetes](../README.md)

Kubernetes networking is the layer that decides how pods communicate, how services receive traffic and how external clients reach workloads.

For this homelab, networking is one of the most important learning areas because it connects Linux, Kubernetes, MikroTik routing, VLANs, DNS and service exposure.

---

## Components

| Component | Role | Documentation |
|---|---|---|
| Cilium | CNI, NetworkPolicy, eBPF observability | [cilium](./cilium) |
| MetalLB | Bare-metal LoadBalancer implementation | [metallb](./metallb) |
| Traefik | Ingress controller and reverse proxy | [traefik](./traefik) |
| Ingress controller | HTTP and HTTPS entrypoint | [ingress](./ingress) |
| cert-manager | Certificate automation | [cert-manager](./cert-manager) |

---

## Baseline Choice

Recommended baseline:

- Cilium for pod networking and network policy
- MetalLB for stable service IPs on bare metal
- Traefik as the first ingress controller for HTTP(S)
- cert-manager for TLS automation

This gives a realistic self-hosted platform without requiring cloud load balancers.
