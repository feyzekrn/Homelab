# MetalLB

[<- Back to Kubernetes Networking](../README.md)

MetalLB provides `LoadBalancer` services in bare-metal Kubernetes clusters.

Cloud Kubernetes platforms usually provide external load balancers automatically. Bare-metal clusters do not, so MetalLB fills that gap by assigning IP addresses from a configured local range.

In Kubernetes, a Service of type `LoadBalancer` asks the infrastructure for an externally reachable IP address. In AWS, Azure, Google Cloud or another managed platform, the cloud provider usually creates the load balancer.

In a bare-metal homelab, there is no cloud load balancer. If a Service asks for type `LoadBalancer`, Kubernetes needs something else to provide the IP address and announce it on the local network. MetalLB does that job.

For this project, MetalLB is the bridge between Kubernetes Services and the MikroTik-managed LAN. It lets an ingress controller such as Traefik receive a stable LAN IP instead of relying on awkward NodePort ports.

---

## Why It Fits

This cluster runs at home on physical hardware. MetalLB makes services reachable on stable LAN IPs without depending on a cloud provider.

It also teaches the difference between Kubernetes service abstractions and real network reachability. A Service existing inside Kubernetes does not automatically mean a laptop on the LAN can reach it.

---

## Used For

- exposing ingress controllers
- exposing selected internal services
- testing real `LoadBalancer` service behavior
- integrating Kubernetes service IPs with MikroTik routing
- reserving predictable addresses for platform entrypoints

---

## Strengths

- Provides cloud-like `LoadBalancer` behavior on bare metal.
- Simple mental model when used with a reserved LAN IP range.
- Works well with ingress controllers such as Traefik.
- Avoids exposing many NodePort services directly.
- Teaches the boundary between cluster networking and physical networking.

---

## Weaknesses

- Requires careful IP range planning to avoid conflicts with DHCP or static addresses.
- Misconfigured L2 or BGP behavior can make services unreachable from the LAN.
- It does not replace ingress routing for HTTP host/path rules.
- It is not a full cloud load balancer with managed health checks and global routing.

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
../../../../helm-charts/networking/metallb/
```

---

## Learning Links

- [MetalLB documentation](https://metallb.universe.tf/)
- [Kubernetes Service documentation](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Wikipedia: Load balancing](https://en.wikipedia.org/wiki/Load_balancing_(computing))
- [Wikipedia: Address Resolution Protocol](https://en.wikipedia.org/wiki/Address_Resolution_Protocol)
