# Cilium

[<- Back to Kubernetes Cluster](../README.md)

Cilium is the recommended CNI for this homelab. It provides pod networking, Kubernetes NetworkPolicy support and eBPF-based visibility into traffic.

A Kubernetes cluster needs a Container Network Interface, usually shortened to CNI. The CNI is the part that makes pod networking work across nodes. Without a working CNI, pods cannot reliably communicate with each other and normal Kubernetes networking will not function.

Cilium is a CNI that uses eBPF, a modern Linux kernel technology that can run safe programs inside the kernel for networking, security and observability. In practice, Cilium can provide pod networking, service routing, network policies and traffic visibility through Hubble.

For beginners, the important point is this: Cilium is not an optional dashboard or app. It is one of the foundational cluster networking components.

---

## Why It Fits

Cilium is useful here because the project is not only about running workloads. It is also about understanding networking. Cilium exposes modern Linux networking concepts such as eBPF, policy enforcement, service routing and observability.

It is a strong learning choice because it can start as the normal CNI and later grow into deeper topics: NetworkPolicy, Hubble flow visibility, L7-aware policy, Gateway API integration and possible service-mesh features.

---

## Used For

- pod-to-pod networking
- Kubernetes NetworkPolicy
- future L7-aware policy experiments
- traffic visibility through Hubble
- learning eBPF-based networking
- possible future Gateway API or service-mesh experiments

---

## Strengths

- Modern eBPF-based networking model.
- Strong NetworkPolicy and observability features.
- Hubble can show service-to-service network flows.
- Widely adopted in modern Kubernetes platforms.
- Can support advanced features later without changing the basic CNI choice.

---

## Weaknesses

- More complex than very small CNIs such as Flannel.
- eBPF concepts can be unfamiliar at first.
- Troubleshooting may require Linux networking knowledge.
- Advanced features should be introduced gradually to avoid making the first cluster hard to debug.

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
../../../helm-charts/infrastructure/kubernetes/cilium/
```

---

## Learning Links

- [Cilium documentation](https://docs.cilium.io/)
- [Cilium Hubble documentation](https://docs.cilium.io/en/stable/observability/hubble/)
- [Wikipedia: eBPF](https://en.wikipedia.org/wiki/EBPF)
- [Kubernetes NetworkPolicy documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
