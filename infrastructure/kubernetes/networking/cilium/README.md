# Cilium

[<- Back to Kubernetes Networking](../README.md)

Cilium is the recommended CNI for this homelab. It provides pod networking, Kubernetes NetworkPolicy support and eBPF-based visibility into traffic.

---

## Why It Fits

Cilium is useful here because the project is not only about running workloads. It is also about understanding networking. Cilium exposes modern Linux networking concepts such as eBPF, policy enforcement, service routing and observability.

---

## Used For

- pod-to-pod networking
- Kubernetes NetworkPolicy
- future L7-aware policy experiments
- traffic visibility through Hubble
- learning eBPF-based networking

---

## Alternatives

| Alternative | Notes |
|---|---|
| Calico | Mature, widely used, strong policy model |
| Flannel | Simple, but too limited for deeper networking learning |
| kube-router | Lightweight, but less common in modern homelab learning paths |

---

## Runtime Status

Cilium is currently `⚫ Inactive`. It should run permanently once the Kubernetes cluster exists. Without a CNI, the cluster cannot provide normal pod networking.

---

## Future Deployment Link

Planned deployment location:

```text
../../../../helm-charts/networking/cilium/
```
