# Kubernetes Networking

[<- Back to Kubernetes](../README.md)

Kubernetes networking is the layer that decides how pods communicate, how services receive traffic and how external clients reach workloads.

For this homelab, networking is one of the most important learning areas because it connects Linux, Kubernetes, MikroTik routing, VLANs, DNS and service exposure.

Kubernetes runs many small workloads across multiple nodes. Those workloads need a network. Pods need to talk to other pods, Services need stable virtual addresses, users need to reach applications and the physical LAN needs to know where exposed services live.

In a cloud provider, many of these pieces are hidden behind managed networking products. In a bare-metal homelab, the cluster owner must provide them. That is why this directory separates the networking concepts:

- Cilium provides the pod network and policy enforcement.
- MetalLB gives `LoadBalancer` services real LAN IP addresses.
- An ingress controller routes HTTP and HTTPS traffic to services.
- cert-manager automates TLS certificates.
- MikroTik networking provides the physical and routed network under the cluster.

---

## Why This Matters

Networking is what turns a set of containers into a usable platform. Pods need to talk to each other, users need to reach applications, services need stable addresses and the physical network needs to understand where traffic should go.

In a homelab, Kubernetes networking is especially valuable because there is no cloud provider hiding the details. You have to understand CNI, LoadBalancer IPs, ingress routing, DNS, TLS and how all of that maps back to the switch and router.

In companies, networking is a shared responsibility between platform, security and application teams. The same concepts appear with more policy, segmentation and audit requirements: ingress, egress, service exposure, certificates, network policies and traffic control.

---

## What You Can Do With It

- give pods a working network
- expose services through stable LAN IPs
- route HTTP(S) traffic through Traefik
- automate TLS certificates
- test NetworkPolicy behavior
- connect Kubernetes service exposure to MikroTik routing
- prepare for future service mesh experiments

---

## Networking Layers

| Layer | Question it answers | Component in this project |
|---|---|---|
| CNI | How do pods get network connectivity? | [`./cilium`](./cilium) |
| Service IPs | How do workloads get stable internal addresses? | Kubernetes Services |
| Bare-metal LoadBalancer | How does a Service get a LAN-reachable IP? | [`./metallb`](./metallb) |
| HTTP routing | How does `grafana.example` reach the right Service? | [`./ingress`](./ingress), [`./traefik`](./traefik) |
| TLS | How are HTTPS certificates created and renewed? | [`./cert-manager`](./cert-manager) |
| Physical network | Which VLAN, route or firewall permits traffic? | [`../../network`](../../network) |

---

## Components

| Path | Role |
|---|---|
| [`./cilium`](./cilium) | CNI, NetworkPolicy, eBPF observability |
| [`./metallb`](./metallb) | Bare-metal LoadBalancer implementation |
| [`./traefik`](./traefik) | Ingress controller and reverse proxy |
| [`./ingress`](./ingress) | HTTP and HTTPS entrypoint concept |
| [`./cert-manager`](./cert-manager) | Certificate automation |

---

## Baseline Choice

Recommended baseline:

- Cilium for pod networking and network policy
- MetalLB for stable service IPs on bare metal
- Traefik as the first ingress controller for HTTP(S)
- cert-manager for TLS automation

This gives a realistic self-hosted platform without requiring cloud load balancers.

---

## Learning Links

- [Wikipedia: Kubernetes](https://en.wikipedia.org/wiki/Kubernetes)
- [Kubernetes networking documentation](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
- [Wikipedia: Reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy)
- [Wikipedia: Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security)
- [Wikipedia: Virtual LAN](https://en.wikipedia.org/wiki/VLAN)
