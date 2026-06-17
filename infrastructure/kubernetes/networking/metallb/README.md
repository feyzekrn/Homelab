# MetalLB

[<- Back to Kubernetes Networking](../README.md)

MetalLB provides `LoadBalancer` services in bare-metal Kubernetes clusters.

Cloud Kubernetes platforms usually provide external load balancers automatically. Bare-metal clusters do not, so MetalLB fills that gap by assigning IP addresses from a configured local range.

---

## Why It Fits

This cluster runs at home on physical hardware. MetalLB makes services reachable on stable LAN IPs without depending on a cloud provider.

---

## Used For

- exposing ingress controllers
- exposing selected internal services
- testing real `LoadBalancer` service behavior
- integrating Kubernetes service IPs with MikroTik routing

---

## Alternatives

| Alternative | Notes |
|---|---|
| kube-vip | Good option for control plane VIPs and service load balancing |
| NodePort | Simple but awkward for stable service exposure |
| Ingress only | Works for HTTP(S), not for arbitrary TCP/UDP services |

---

## Runtime Status

MetalLB is currently `⚫ Inactive`. It should run permanently once external service exposure is needed.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/platform/metallb/
```
